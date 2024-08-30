## Py Transcode

I have many videos, most of my devices can decode AV1 so for storage sake, this is designed to transcode video files located in the specified dirs.

### How to Use

This assumes Python is called with the `python` command. If you run python with `python3`, substitute with that. This also assumes `pip` as the package manager and `venv` as the virtual environment, make any adjustments for your use.
- Make sure you have Python >3.10 installed: `python -v` or `python3 -v`
- Install the requirements `pip install -r requirements.txt`
- Run the app `python run.py -h` for help with arguments

### TODO

- [ ] Detect video codec, only transcode files that aren't already av1
- [ ] Filesystem watch dir feature to auto transcode videos as they're added to specific folders.