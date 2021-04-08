import ffmpeg

start=5
end=20
extra=5

overlay_file = (
    ffmpeg
    .input('overlay.jpg', loop=1, t=end-start)
    .filter('scale', 120, -1)
    .drawtext(
        text='Lucas', fontfile='Kiss Boom.ttf',
        x=10, y=100,
        fontsize='42', fontcolor='white',
        bordercolor='black', borderw=1,
    )
    .drawbox(0, 0, 120, 135, color='red', thickness=5)
    .filter('fade', 'in', 200, 1, d=(end-start)/4, alpha=1)
    .setpts('PTS-STARTPTS')
)

x=80
y=50
in_file = ffmpeg.input('input.webm')
edit = (
    in_file
    .video
    .trim(start=start, end=end)
    .overlay(overlay_file, x=x, y=y)
    .setpts('PTS-STARTPTS')
)

final = ffmpeg.concat(
        in_file.trim(start=0, end=start).setpts('PTS-STARTPTS'),
        edit,
        in_file.trim(start=end, end=end+extra).setpts('PTS-STARTPTS'),
)

audio = (
    in_file.audio
    .filter_('atrim', start=0, end=end+extra)
    .filter_('asetpts', 'PTS-STARTPTS')
)

ffmpeg.output(
    audio,
    final,
    'out.mp4',
).overwrite_output().run()
