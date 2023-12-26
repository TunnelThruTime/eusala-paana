
import os
from rich.console import Console

breakpoint()


console = Console()
rel = os.path.join(os.path.dirname(__file__), '..')
git_root = os.path.abspath(rel)
console.rule('seg')
print(__file__)
print(rel)
print(git_root)


current_script_path = os.path.abspath(__file__)
git_root_relative = os.path.join(current_script_path, '..')
git_root = os.path.dirname(current_script_path)

print(current_script_path)
print(git_root_relative)
print(git_root)


# def prompt_and_execute():
   # user_input = input("Send off email? (Y/N): ")
   # if user_input.upper() == "Y":
       # # Execute your email sending code or desired task here
       # print("Email sent!")
   # else:
       # print("Email not sent.")
   # sys.exit(0)
# scheduler = BlockingScheduler()

# scheduler.add_job(prompt_and_execute, 'interval', minutes=30)

# try:
   # scheduler.start()
# except KeyboardInterrupt:
   # pass
