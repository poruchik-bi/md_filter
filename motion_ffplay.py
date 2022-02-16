import ffmpeg
stream = ffmpeg.input('/home/er/workspace/md_filter/10.0.6.25_04_20220212124853446.mp4')
stream = ffmpeg.hflip(stream)
stream = ffmpeg.output(stream, 'output.mp4')
ffmpeg.run(stream)