import io
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext

from src.Osintgram import Osintgram
from src import config


def run_gui():
    root = tk.Tk()
    root.title("Osintgram GUI")

    tk.Label(root, text="Username:").grid(row=0, column=0, sticky="e")
    username_var = tk.StringVar()
    tk.Entry(root, textvariable=username_var).grid(row=0, column=1, padx=5, pady=2)

    tk.Label(root, text="Password:").grid(row=1, column=0, sticky="e")
    password_var = tk.StringVar()
    tk.Entry(root, textvariable=password_var, show="*").grid(row=1, column=1, padx=5, pady=2)

    tk.Label(root, text="Target:").grid(row=2, column=0, sticky="e")
    target_var = tk.StringVar()
    tk.Entry(root, textvariable=target_var).grid(row=2, column=1, padx=5, pady=2)

    file_var = tk.BooleanVar()
    tk.Checkbutton(root, text="FILE", variable=file_var).grid(row=3, column=0, sticky="w", padx=5)
    json_var = tk.BooleanVar()
    tk.Checkbutton(root, text="JSON", variable=json_var).grid(row=3, column=1, sticky="w", padx=5)

    tk.Label(root, text="Command:").grid(row=4, column=0, sticky="e")
    command_var = tk.StringVar()
    command_box = ttk.Combobox(root, textvariable=command_var, width=25)
    command_box.grid(row=4, column=1, padx=5, pady=2)

    output_area = scrolledtext.ScrolledText(root, width=60, height=20)
    output_area.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    def run_command():
        user = username_var.get()
        pwd = password_var.get()
        tgt = target_var.get()
        cmd = command_var.get()
        config.config["Credentials"] = {"username": user, "password": pwd}
        api = Osintgram(tgt, file_var.get(), json_var.get(), cmd, None, False)
        commands = {
            'addrs':            api.get_addrs,
            'cache':            api.clear_cache,
            'captions':         api.get_captions,
            'commentdata':      api.get_comment_data,
            'comments':         api.get_total_comments,
            'followers':        api.get_followers,
            'followings':       api.get_followings,
            'fwersemail':       api.get_fwersemail,
            'fwingsemail':      api.get_fwingsemail,
            'fwersnumber':      api.get_fwersnumber,
            'fwingsnumber':     api.get_fwingsnumber,
            'hashtags':         api.get_hashtags,
            'info':             api.get_user_info,
            'likes':            api.get_total_likes,
            'mediatype':        api.get_media_type,
            'photodes':         api.get_photo_description,
            'photos':           api.get_user_photo,
            'propic':           api.get_user_propic,
            'stories':          api.get_user_stories,
            'tagged':           api.get_people_tagged_by_user,
            'target':           api.change_target,
            'wcommented':       api.get_people_who_commented,
            'wtagged':          api.get_people_who_tagged,
        }
        command_box['values'] = list(commands.keys())
        func = commands.get(cmd)
        if func:
            buffer = io.StringIO()
            old_stdout = sys.stdout
            sys.stdout = buffer
            try:
                res = func()
            finally:
                sys.stdout = old_stdout
            text = buffer.getvalue()
            if res:
                text += str(res)
        else:
            text = "Unknown command"
        output_area.delete('1.0', tk.END)
        output_area.insert(tk.END, text)

    tk.Button(root, text="Run", command=run_command).grid(row=5, column=0, columnspan=2, pady=5)

    root.mainloop()


if __name__ == "__main__":
    run_gui()
