import subprocess, sys, json, numpy as np, re
for f in sys.argv[1:]:
    pr=json.loads(subprocess.run(['ffprobe','-v','error','-count_frames','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_read_frames,color_range,color_space,color_primaries,color_transfer,duration,sample_rate','-show_entries','format=duration','-of','json',f],capture_output=True,text=True).stdout)
    v=[s for s in pr['streams'] if s['codec_type']=='video'][0]
    # decode first & last frame to rgb (bt709 tv -> full rgb)
    def frame(sel):
        r=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf',f"select='eq(n\\,{sel})',scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24",'-frames:v','1','-f','rawvideo','-'],capture_output=True).stdout
        return np.frombuffer(r,np.uint8).reshape(v['height'],v['width'],3)
    a=frame(0); z=frame(int(v['nb_read_frames'])-1)
    y=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf','signalstats,metadata=print:key=lavfi.signalstats.YMIN:file=-,format=yuv420p','-f','null','-'],capture_output=True,text=True).stdout
    ymin=min(int(float(x)) for x in re.findall(r'YMIN=([\d.]+)',y)); 
    y2=subprocess.run(['ffmpeg','-v','error','-i',f,'-vf','signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=-','-f','null','-'],capture_output=True,text=True).stdout
    ymax=max(int(float(x)) for x in re.findall(r'YMAX=([\d.]+)',y2))
    eb=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',f,'-vn','-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True).stderr
    I=re.findall(r'I:\s+(-?[\d.]+) LUFS',eb)[-1]; TP=re.findall(r'Peak:\s+(-?[\d.]+) dBFS',eb)[-1]
    print(f"{f}: {v['width']}x{v['height']} {v['r_frame_rate']} frames={v['nb_read_frames']} dur={pr['format']['duration']} range={v.get('color_range')} space={v.get('color_space')} prim={v.get('color_primaries')} trc={v.get('color_transfer')}")
    print(f"   bg corner f0={a[5,5].tolist()} last={z[5,5].tolist()} | Y range {ymin}-{ymax} | audio I={I} LUFS TP={TP} dBTP")
