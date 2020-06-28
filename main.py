import cv2
from predict import process, get_total, get_countries, get_news
from flask import Flask, render_template, Response

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        
        success, image = self.video.read()
        image, num_mask, num_no_mask = process(image)
        
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera')
def camera():
    return render_template('elements.html')

@app.route('/stats')
def stats():
    countries = get_countries()
    tot = get_total()
    return render_template('stats.html', 
                            total = tot, 
                            countries=["Countries"] + countries[0][0:10], 
                            cases = ["Number of Cases"] + countries[1][0:10], 
                            deaths = ["Number of Deaths"] + countries[2][0:10])

@app.route('/feed')
def feed():
    news = get_news()
    return render_template('feed.html', 
                            news=news)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    