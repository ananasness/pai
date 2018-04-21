import os
import subprocess
import tempfile


def convert_to_flac(in_bytes, out_file_name):
    temp_in_file = tempfile.NamedTemporaryFile(delete=False)
    temp_in_file.write(in_bytes)
    in_filename = temp_in_file.name
    temp_in_file.close()

    command = [
        r'/Users/almiramurtazina/git/pai/tic-tac-toe/ffmpeg/bin/ffmpeg',
        '-i', in_filename,
        '-c:a', 'flac',
        '-ar', '16000',
        out_file_name
    ]

    proc = subprocess.Popen(command, stderr=subprocess.DEVNULL)
    proc.wait()

    os.remove(in_filename)
