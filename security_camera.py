import datetime
import cv2
import os
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo


def update_duration(event):
  duration = vid_player.video_info()["duration"]
  end_time["text"] = str(datetime.timedelta(seconds=duration))
  progress_slider["to"] = duration


def update_scale(event):
  progress_value.set(vid_player.current_duration())


def load_video():
  file_path = filedialog.askopenfilename()

  if file_path:
    vid_player.load(file_path)

    progress_slider.config(to=0, from_=0)
    play_pause_btn["text"] = "Play"
    progress_value.set(0)


def seek(value):
  vid_player.seek(int(value))


def skip(value: int):
  vid_player.seek(int(progress_slider.get()) + value)
  progress_value.set(progress_slider.get() + value)


def paly_pause():
  if vid_player.is_paused():
    vid_player.play()
    play_pause_btn["text"] = "Pause"

  else:
    vid_player.pause()
    play_pause_btn["text"] = "Play"


def video_ended(event):
  progress_slider.set(progress_slider["to"])
  play_pause_btn["text"] = "Play"
  progress_slider.set(0)


def video_stop():
  vid_player.stop()


def webcam():
  cap = cv2.VideoCapture(0)

  face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
  body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

  if not os.path.exists('detections'):
    os.mkdir('detections')

  while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, width, height) in faces:
      cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)
      face_roi = frame[y:y + height, x:x + width]

      if not os.path.exists('detections/' + datetime.datetime.now().strftime('%Y-%m-%d')):
        os.mkdir('detections/' + datetime.datetime.now().strftime('%Y-%m-%d'))

      cv2.imwrite('detections/' + datetime.datetime.now().strftime('%Y-%m-%d') + '/' + datetime.datetime.now().strftime('%H-%M') + '.jpg', face_roi)

    cv2.imshow('Live Feed Camera', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break


root =tk.Tk()
root.title("Surveillance Camera")
root.geometry("900x450")

frame = tk.Frame(root)
frame.pack()

# Left side

left_frame = tk.Frame(root)
left_frame.pack(side=LEFT)

right_frame = tk.Frame(root)
right_frame.pack(side=RIGHT)

vid_player = TkinterVideo(scaled=True, master=left_frame)
vid_player.grid(row=0, column=0, columnspan=5)

load_btn = tk.Button(left_frame, text="Load", command=load_video)
load_btn.grid(row=1, column=0)

exit_btn = tk.Button(left_frame, text="Exit", command=root.destroy)
exit_btn.grid(row=1, column=1)

play_pause_btn = tk.Button(left_frame, text="Play", command=paly_pause)
play_pause_btn.grid(row=1, column=2)

stop_btn = tk.Button(left_frame, text="Stop", command=video_stop)
stop_btn.grid(row=1, column=3)

skip_plus_5sec = tk.Button(left_frame, text="Skip -5 sec", command=lambda: skip(-5))
skip_plus_5sec.grid(row=2, column=0)

start_time = tk.Label(left_frame, text=str(datetime.timedelta(seconds=0)))
start_time.grid(row=2, column=1)

progress_value = tk.IntVar(left_frame)

progress_slider = tk.Scale(left_frame, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
progress_slider.grid(row=2, column=2)

end_time = tk. Label(left_frame, text=str(datetime.timedelta(seconds=0)))
end_time.grid(row=2, column=3)

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

skip_plus_5sec = tk.Button(left_frame, text="Skip +5 sec", command=lambda: skip(5))
skip_plus_5sec.grid(row=2, column=4)

# Right side

webcam_btn = tk.Button(right_frame, text="webcam", command=webcam)
webcam_btn.grid(row=0, column=0)

root.mainloop()