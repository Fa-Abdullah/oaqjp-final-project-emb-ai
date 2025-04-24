"""
server.py

This module implements a Flask web application for emotion detection.
It provides an endpoint `/emotionDetector` that accepts text input via a POST request,
analyzes the emotions in the text using the `emotion_detector` function, and returns
the results in a formatted response.
"""

from flask import Flask, request, render_template
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

@app.route("/emotionDetector", methods=['POST'])
def sent_analyzer():
    """Handles POST requests to the /emotionDetector endpoint."""
    try:
        # Get the input text from the POST request
        input_data = request.get_json()
        if not input_data or 'text' not in input_data:
            return {"error": "Invalid input. Please provide a 'text' key in the JSON body."}, 400

        text_to_analyze = input_data['text']

        # Call the emotion_detector function
        result = emotion_detector(text_to_analyze)

        # Check for errors in the result
        if 'error' in result:
            return {"None": result['error']}, 400

        if result['dominant_emotion'] is None:
            return "Invalid text! Please try again!"

        # Format the response using the result from emotion_detector
        response_text = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

        return response_text

    except Exception as e:
        # Catch any unexpected errors
        return {
                "error": f"An unexpected error occurred:{str(e)}"
                }, 500

@app.route("/")
#call html file
def render_index_page():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
