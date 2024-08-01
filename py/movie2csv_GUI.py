import cv2
import pytesseract
import os
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox
from tkinter import ttk
import numpy as np

# Specify the installation path of Tesseract (if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Video to CSV Converter")
        
        self.video_path = ""
        self.csv_path = ""
        self.save_dir = ""
        self.interval = 1.0
        self.regions = []
        self.labels = []
        self.exp_setting=""
        self.imp_setting=""
        
        self.create_widgets()
    
    def create_widgets(self):
        # Button to select video file
        self.btn_select_video = tk.Button(self.root, text="Select Video File", command=self.select_video)
        self.btn_select_video.grid(row=0, column=0, padx=10, pady=10)
        
        # Display selected video file
        self.lbl_video_path = tk.Label(self.root, text="No file selected")
        self.lbl_video_path.grid(row=0, column=1, padx=10, pady=10)
        
        # Button to select CSV file
        self.btn_select_csv = tk.Button(self.root, text="Select CSV File", command=self.select_csv)
        self.btn_select_csv.grid(row=1, column=0, padx=10, pady=10)
        
        # Display selected CSV file
        self.lbl_csv_path = tk.Label(self.root, text="No file selected")
        self.lbl_csv_path.grid(row=1, column=1, padx=10, pady=10)
        
        # Button to select save directory
        self.btn_select_dir = tk.Button(self.root, text="Select Save Directory", command=self.select_directory)
        self.btn_select_dir.grid(row=2, column=0, padx=10, pady=10)
        
        # Display selected directory
        self.lbl_save_dir = tk.Label(self.root, text="No directory selected")
        self.lbl_save_dir.grid(row=2, column=1, padx=10, pady=10)
        
        # Capture interval setting
        self.lbl_interval = tk.Label(self.root, text="Capture Interval (seconds):")
        self.lbl_interval.grid(row=3, column=0, padx=10, pady=10)
        self.entry_interval = tk.Entry(self.root)
        self.entry_interval.grid(row=3, column=1, padx=10, pady=10)
        self.entry_interval.insert(0, "1")
        
        # Capture region setting
        self.btn_add_region = tk.Button(self.root, text="Add Capture Region", command=self.add_region)
        self.btn_add_region.grid(row=4, column=0, padx=10, pady=10)

        # Capture region setting
        self.btn_add_region = tk.Button(self.root, text="Edit Capture Region", command=self.edit_region)
        self.btn_add_region.grid(row=5, column=0, padx=10, pady=10)
        
        # Capture region setting export
        self.btn_add_region = tk.Button(self.root, text="Export Capture Region", command=self.export_region)
        self.btn_add_region.grid(row=6, column=0, padx=10, pady=10)
        self.lbl_export_path = tk.Label(self.root, text="No file selected")
        self.lbl_export_path.grid(row=6, column=1, padx=10, pady=10)
        #self.setting_file_out = tk.Entry(self.root)
        #self.setting_file_out.grid(row=6, column=1, padx=10, pady=10)
        #self.setting_file_out.insert(0, "hoge.csv")

        # Capture region setting import
        self.btn_add_region = tk.Button(self.root, text="Import Capture Region", command=self.import_region)
        self.btn_add_region.grid(row=7, column=0, padx=10, pady=10)
        self.lbl_import_path = tk.Label(self.root, text="No file selected")
        self.lbl_import_path.grid(row=7, column=1, padx=10, pady=10)
        
        # Display current capture regions
        self.lbl_regions = tk.Label(self.root, text="No regions specified")
        self.lbl_regions.grid(row=4, column=1, padx=10, pady=10)
        
        # Button to show the capture
        self.btn_show_capture = tk.Button(self.root, text="Show Capture", command=self.show_capture)
        self.btn_show_capture.grid(row=8, column=0, padx=10, pady=10)
        
        # Start button
        self.btn_start = tk.Button(self.root, text="Start", command=self.start)
        self.btn_start.grid(row=8, column=1, pady=20)
    
    def select_video(self):
        self.video_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi")])
        self.lbl_video_path.config(text=self.video_path)
    
    def select_csv(self):
        self.csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        self.lbl_csv_path.config(text=self.csv_path)
    
    def select_directory(self):
        self.save_dir = filedialog.askdirectory()
        self.lbl_save_dir.config(text=self.save_dir)
    
    #def add_region(self):
    #    x = simpledialog.askinteger("Input", "Enter x coordinate:")
    #    y = simpledialog.askinteger("Input", "Enter y coordinate:")
    #    w = simpledialog.askinteger("Input", "Enter width:")
    #    h = simpledialog.askinteger("Input", "Enter height:")
    #    label = simpledialog.askstring("Input", "Enter label for this region:")
    #    
    #    if None not in (x, y, w, h, label):
    #        self.regions.append((x, y, w, h))
    #        self.labels.append(label)
    #        self.lbl_regions.config(text=f"{len(self.regions)} regions specified")
    #    else:
    #        messagebox.showerror("Error", "All fields must be filled in")
    def add_region(self):
      def save_region():
          try:
              x = int(entry_x.get())
              y = int(entry_y.get())
              w = int(entry_w.get())
              h = int(entry_h.get())
              label = entry_label.get()

              self.regions.append((x, y, w, h))
              self.labels.append(label)
              self.lbl_regions.config(text=f"{len(self.regions)} regions specified")
              input_window.destroy()
              self.update_region_listbox()
          except ValueError:
              messagebox.showerror("Error", "Please enter valid integers for x, y, width, and height")

      # Create a new window for input
      input_window = tk.Toplevel(self.root)
      input_window.title("Add Capture Region")

      # Labels and entries for x, y, width, height, and label
      tk.Label(input_window, text="x coordinate:").grid(row=0, column=0, padx=10, pady=5)
      entry_x = tk.Entry(input_window)
      entry_x.grid(row=0, column=1, padx=10, pady=5)

      tk.Label(input_window, text="y coordinate:").grid(row=1, column=0, padx=10, pady=5)
      entry_y = tk.Entry(input_window)
      entry_y.grid(row=1, column=1, padx=10, pady=5)

      tk.Label(input_window, text="width:").grid(row=2, column=0, padx=10, pady=5)
      entry_w = tk.Entry(input_window)
      entry_w.grid(row=2, column=1, padx=10, pady=5)

      tk.Label(input_window, text="height:").grid(row=3, column=0, padx=10, pady=5)
      entry_h = tk.Entry(input_window)
      entry_h.grid(row=3, column=1, padx=10, pady=5)

      tk.Label(input_window, text="label:").grid(row=4, column=0, padx=10, pady=5)
      entry_label = tk.Entry(input_window)
      entry_label.grid(row=4, column=1, padx=10, pady=5)

      # Save button
      btn_save = tk.Button(input_window, text="Save", command=save_region)
      btn_save.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_region(self):
      def update_region():
          try:
              index = region_listbox.curselection()[0]
              x = int(entry_x.get())
              y = int(entry_y.get())
              w = int(entry_w.get())
              h = int(entry_h.get())
              label = entry_label.get()

              self.regions[index] = (x, y, w, h)
              self.labels[index] = label
              input_window.destroy()
              self.update_region_listbox()
          except ValueError:
              messagebox.showerror("Error", "Please enter valid integers for x, y, width, and height")
          except IndexError:
              messagebox.showerror("Error", "Please select a region to edit")

      def delete_region():
          try:
              index = region_listbox.curselection()[0]
              del self.regions[index]
              del self.labels[index]
              input_window.destroy()
              self.update_region_listbox()
          except IndexError:
              messagebox.showerror("Error", "Please select a region to delete")

      if not self.regions:
          messagebox.showerror("Error", "No regions to edit")
          return

      # Create a new window for input
      input_window = tk.Toplevel(self.root)
      input_window.title("Edit Capture Region")

      region_listbox = tk.Listbox(input_window)
      region_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

      for i, (region, label) in enumerate(zip(self.regions, self.labels)):
          region_listbox.insert(tk.END, f"{label}: {region}")

      # Labels and entries for x, y, width, height, and label
      tk.Label(input_window, text="x coordinate:").grid(row=1, column=0, padx=10, pady=5)
      entry_x = tk.Entry(input_window)
      entry_x.grid(row=1, column=1, padx=10, pady=5)

      tk.Label(input_window, text="y coordinate:").grid(row=2, column=0, padx=10, pady=5)
      entry_y = tk.Entry(input_window)
      entry_y.grid(row=2, column=1, padx=10, pady=5)

      tk.Label(input_window, text="width:").grid(row=3, column=0, padx=10, pady=5)
      entry_w = tk.Entry(input_window)
      entry_w.grid(row=3, column=1, padx=10, pady=5)

      tk.Label(input_window, text="height:").grid(row=4, column=0, padx=10, pady=5)
      entry_h = tk.Entry(input_window)
      entry_h.grid(row=4, column=1, padx=10, pady=5)

      tk.Label(input_window, text="label:").grid(row=5, column=0, padx=10, pady=5)
      entry_label = tk.Entry(input_window)
      entry_label.grid(row=5, column=1, padx=10, pady=5)

      # Update and delete buttons
      btn_update = tk.Button(input_window, text="Update", command=update_region)
      btn_update.grid(row=6, column=0, pady=10)

      btn_delete = tk.Button(input_window, text="Delete", command=delete_region)
      btn_delete.grid(row=6, column=1, pady=10)

    def export_region(self):
      self.exp_setting=filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
      self.lbl_export_path.config(text=self.exp_setting)
      #self.exp_setting=self.setting_file_out.get()

      np_regions=np.asarray(self.regions)
      np_labels =np.asarray(self.labels)
      np_regions_T=np_regions.T
      np_labels_T =np_labels .T
      np_regions_labels=np.vstack([np_regions_T,np_labels_T])

      df_ex=pd.DataFrame(np_regions_labels.T,columns=['X','Y','W','H','Label'])
      df_ex.to_csv(self.exp_setting,index=False)
      print(f"{self.exp_setting} is exported.")


    def import_region(self):
      self.imp_setting = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
      self.lbl_import_path.config(text=self.imp_setting)
      df_im=pd.read_csv(self.imp_setting)
      print(df_im)
      self.regions=df_im[['X','Y','W','H']].apply(lambda x: x.tolist(), axis=1).tolist()
      self.labels =df_im['Label'].tolist()
      print(self.regions)
      print(self.labels)

      self.update_region_listbox()

    def update_region_listbox(self):
      # Update the region listbox (if it exists) with the current regions and labels
      try:
          self.region_listbox.delete(0, tk.END)
          for i, (region, label) in enumerate(zip(self.regions, self.labels)):
              self.region_listbox.insert(tk.END, f"{label}: {region}")
      except AttributeError:
          pass
   
    def start(self):
        try:
            self.interval = float(self.entry_interval.get())
        except ValueError:
            messagebox.showerror("Error", "Interval must be an integer")
            return
        
        if not self.video_path or not self.csv_path or not self.save_dir or not self.regions:
            messagebox.showerror("Error", "Please specify all inputs")
            return
        
        self.process_video()
    
    def show_capture(self):
        if not self.video_path:
            messagebox.showerror("Error", "Please select a video file first")
            return

        # Open the video file
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video")
            return

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Could not read the first frame")
            return
        def mouse_callback(event, x, y, flags, param):
            if event == cv2.EVENT_MOUSEMOVE:
                temp_frame = frame.copy()
                for x_r, y_r, w_r, h_r in self.regions:
                    cv2.rectangle(temp_frame, (x_r, y_r), (x_r + w_r, y_r + h_r), (255, 0, 0), 2)
                cv2.putText(temp_frame, f'X: {x}, Y: {y}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
                cv2.imshow("Capture Preview", temp_frame)

        cv2.namedWindow("Capture Preview")
        cv2.setMouseCallback("Capture Preview", mouse_callback)
        
        for x, y, w, h in self.regions:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow("Capture Preview", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cap.release()
    
    def process_video(self):
        # Open the video file
        cap = cv2.VideoCapture(self.video_path)

        if not cap.isOpened():
            messagebox.showerror("Error", "Could not open video")
            return

        # Get the frame rate of the video
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_interval = int(fps * self.interval)

        frame_count = 0
        data = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % frame_interval == 0:
                row = []
                whole_frame_filename = os.path.join(self.save_dir, f"whole_frame_{frame_count // frame_interval}.png")
                cv2.imwrite(whole_frame_filename, frame)
                for i, (region,label) in enumerate(zip(self.regions,self.labels)):
                    x, y, w, h = region
                    roi = frame[y:y+h, x:x+w]

                    # Save the file with a specified name
                    frame_filename = os.path.join(self.save_dir, f"frame_{label}_{frame_count // frame_interval}.png")
                    cv2.imwrite(frame_filename, roi)
                    print(f"Saved {frame_filename}")

                    # Apply OCR and read the number
                    text = pytesseract.image_to_string(roi, config='--psm 7')
                    print(f"Detected text: {text}")
                    row.append(text)
                
                data.append(row)

            frame_count += 1

        cap.release()
        cv2.destroyAllWindows()

        # Save data to CSV
        df = pd.DataFrame(data, columns=self.labels)
        print(df)
        df.to_csv(self.csv_path,index=False)
        #with open(self.csv_path, 'w', newline='') as csvfile:
        #    writer = csv.writer(csvfile)
        #    writer.writerow(self.labels)
        #    writer.writerows(data)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

