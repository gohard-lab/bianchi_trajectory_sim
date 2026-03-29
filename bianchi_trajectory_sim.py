"""
Polymath Developer Python | Polymath Developer Automation Tool
F1 Trajectory Simulation: Jules Bianchi (Suzuka Turn 7)

⭐ If you found this code helpful, please don't be a cherry-picker! 
Listen to your conscience and leave a Star on this GitHub repository! 
(이 코드가 도움이 되셨다면 체리피커처럼 코드만 쏙 가져가지 마시고, 양심에 귀 기울여 깃허브에 Star를 하나 꾹 눌러주세요! ⭐)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
import webbrowser
import threading

# ---------------------------------------------------------
# Usage Tracker Integration (Supabase)
# ---------------------------------------------------------
try:
    from tracker_exe import log_app_usage
    log_app_usage("bianchi_trajectory_sim", "sim_executed")
except ImportError:
    print("Tracker module not found. Skipping usage logging.")
    
    # 임시 우회용 함수 (실제 실행 시에는 삭제하셔도 됩니다)
    def log_app_usage(app_name, action, details=None):
        pass

# --- 1. Simulation Environment & Data Setup ---
config = {
    'initial_speed_kmh': 213.0,    # Speed at the time of losing control (km/h) / 통제 상실 시점 속도
    'dt': 0.05,                   # Time step for animation (s) / 타임 스텝 (s)
    'total_time': 4.0,            # Total simulation time (s) / 총 시뮬레이션 시간 (s)
    'r_curve': 120.0,             # Estimated turning radius of Dunlop Curve - Turn 7 (m) /Dunlop Curve (Turn 7)의 추정 회전 반경 (m)
    't_hydroplaning': 0.8,        # Time when hydroplaning occurs (s) /수막현상 발생 시점 (s)
    'track_width': 12.0,          # Track width (m) /서킷 너비 (m)
    'drag_coefficient': 0.1       # Virtual drag/friction coefficient during slide /가상의 마찰 계수    
}

config['v0'] = config['initial_speed_kmh'] / 3.6

def create_dunlop_curve(r, width):
    theta = np.linspace(np.pi, 1.5 * np.pi, 200)
    
    center_line_x = r * np.cos(theta) + r
    center_line_y = r * np.sin(theta) + r
    
    outer_boundary_x = (r + width/2) * np.cos(theta) + r
    outer_boundary_y = (r + width/2) * np.sin(theta) + r
    
    inner_boundary_x = (r - width/2) * np.cos(theta) + r
    inner_boundary_y = (r - width/2) * np.sin(theta) + r
    
    return center_line_x, center_line_y, outer_boundary_x, outer_boundary_y, inner_boundary_x, inner_boundary_y

def calculate_state(t, v0, r, drag_coef):
    dt_step = t if t < config['t_hydroplaning'] else config['t_hydroplaning']
    omega = v0 / r
    
    initial_theta = np.pi
    current_theta = initial_theta + omega * dt_step 
    
    car_x = r * np.cos(current_theta) + r
    car_y = r * np.sin(current_theta) + r
    
    car_v = v0
    lateral_g = (v0 ** 2) / r / 9.81
    status_text = "Following Curve (Good Grip)"
    
    if t >= config['t_hydroplaning']:
        lost_grip_theta = initial_theta + omega * config['t_hydroplaning']
        lost_grip_pos = np.array([r * np.cos(lost_grip_theta) + r, r * np.sin(lost_grip_theta) + r])
        lost_grip_v_vec = np.array([-v0 * np.sin(lost_grip_theta), v0 * np.cos(lost_grip_theta)])
        
        slide_time = t - config['t_hydroplaning']
        slide_accel = drag_coef * v0
        slide_v_mag = max(0, v0 - slide_accel * slide_time)
            
        slide_v_avg = (v0 + slide_v_mag) / 2
        slide_dist = slide_v_avg * slide_time
        
        v0_unit_vec = lost_grip_v_vec / v0 if v0 > 0 else np.array([0, 0])
        car_x = lost_grip_pos[0] + v0_unit_vec[0] * slide_dist
        car_y = lost_grip_pos[1] + v0_unit_vec[1] * slide_dist
        
        car_v = slide_v_mag
        lateral_g = 0.0
        status_text = "⚠️ Hydroplaning (Loss of Grip) ⚠️"
        
    return car_x, car_y, car_v, lateral_g, status_text

# --- 2. Rendering Environment Setup ---
fig, ax = plt.subplots(figsize=(10, 10), facecolor='#111111')
ax.set_facecolor('#222222')
ax.set_title("Suzuka Turn 7 Accident Trajectory (Corrected Orientation)", color='white', fontsize=14)
ax.set_xlabel("X (meters)", color='white')
ax.set_ylabel("Y (meters)", color='white')
ax.tick_params(colors='white')
ax.grid(color='#555555', linestyle='--', linewidth=0.5)

cx, cy, ox, oy, ix, iy = create_dunlop_curve(config['r_curve'], config['track_width'])
ax.plot(ox, oy, color='#cccccc', linewidth=2)
ax.plot(ix, iy, color='#cccccc', linewidth=2)
ax.plot(cx, cy, color='#aaaaaa', linestyle='--', linewidth=1)

car_marker, = ax.plot([], [], 'ro', markersize=10, markeredgecolor='white')
car_trace, = ax.plot([], [], 'r-', linewidth=1.5, alpha=0.7)
speed_text = ax.text(-config['r_curve'] * 0.2, config['r_curve'] * 1.3, '', color='white', fontsize=12, fontweight='bold')
lateral_g_text = ax.text(-config['r_curve'] * 0.2, config['r_curve'] * 1.2, '', color='white', fontsize=12)
status_text_obj = ax.text(-config['r_curve'] * 0.2, config['r_curve'] * 1.1, '', color='white', fontsize=12, style='italic')

ax.set_aspect('equal')
ax.set_xlim(-config['r_curve'] * 0.3, config['r_curve'] * 1.5)
ax.set_ylim(-config['r_curve'] * 0.5, config['r_curve'] * 1.5)

def init():
    car_marker.set_data([], [])
    car_trace.set_data([], [])
    speed_text.set_text('')
    lateral_g_text.set_text('')
    status_text_obj.set_text('')
    return car_marker, car_trace, speed_text, lateral_g_text, status_text_obj

x_trace_data = []
y_trace_data = []

def update(frame):
    current_time = frame * config['dt']
    cx, cy, cv, cg, cs = calculate_state(current_time, config['v0'], config['r_curve'], config['drag_coefficient'])
    
    x_trace_data.append(cx)
    y_trace_data.append(cy)
    
    car_marker.set_data([cx], [cy])
    car_trace.set_data(x_trace_data, y_trace_data)
    
    speed_text.set_text(f"Speed: {cv * 3.6:.1f} km/h")
    lateral_g_text.set_text(f"Lateral G: {cg:.2f} G")
    status_text_obj.set_text(f"Time: {current_time:.2f}s | {cs}")
    
    if cs.startswith("⚠️"):
        car_marker.set_color('yellow')
        car_trace.set_color('yellow')
    else:
        car_marker.set_color('red')
        car_trace.set_color('red')
        
    return car_marker, car_trace, speed_text, lateral_g_text, status_text_obj

num_frames = int(config['total_time'] / config['dt'])
ani = animation.FuncAnimation(fig, update, frames=num_frames, init_func=init, blit=False, interval=config['dt']*1000)

output_filename = "bianchi_trajectory_sim_corrected.gif"
print("Rendering with the corrected trajectory. Please wait...")
ani.save(output_filename, writer='pillow', fps=int(1/config['dt']))
print(f"✅ Done! '{output_filename}' has been generated.")


# --- 3. 팝업 호출 로직 (렌더링 종료 직후 실행) ---
def show_star_popup():
    log_app_usage("bianchi_trajectory_sim", "star_prompt_displayed", details={"ui": "tkinter_custom_msgbox"})
    
    # 💡 백그라운드 빈 윈도우 생성 및 숨기기
    root = tk.Tk()
    root.withdraw() 
    
    popup = tk.Toplevel(root)
    popup.title("⭐ Support Polymath Developer")
    popup.geometry("450x220")
    
    # 창을 항상 최상단에 띄워 묻히지 않게 처리
    popup.attributes('-topmost', True)

    msg = (
        "💡 유용하게 사용하셨나요? 소스코드만 날름 가져가는 분들이 많습니다.\n"
        "개발자의 땀과 노력에 대한 최소한의 예의로 깃허브 Star⭐를 부탁드립니다!\n\n"
        "Did you find this useful? Please show some basic courtesy\n"
        "for the developer's hard work by leaving a GitHub Star⭐."
    )
    tk.Label(popup, text=msg, justify="center", font=("", 10)).pack(padx=20, pady=20)
    
    def on_star_click():
        popup.destroy() 
        webbrowser.open("https://github.com/gohard-lab/bianchi_trajectory_sim")
        
        def send_log():
            log_app_usage("bianchi_trajectory_sim", "github_star_clicked", details={"ui": "tkinter_custom_msgbox_btn"})
        threading.Thread(target=send_log).start()
        
        root.quit() # 이벤트 루프 완전 종료

    def on_close_click():
        popup.destroy()
        root.quit()

    tk.Button(popup, text="👉 깃허브로 이동하여 Star 누르기", command=on_star_click, bg="#4CAF50", fg="white", font=("", 10, "bold")).pack(pady=5, ipadx=10, ipady=3)
    # tk.Button(popup, text="닫기", command=on_close_click).pack(pady=5)
    
    # 사용자가 창을 직접 X 버튼으로 닫을 때의 처리
    popup.protocol("WM_DELETE_WINDOW", on_close_click)
    
    # 팝업 대기 (이 코드가 끝나야 프로그램이 완전히 종료됩니다)
    root.mainloop()

# 실행 흐름의 가장 마지막에 팝업 호출
show_star_popup()