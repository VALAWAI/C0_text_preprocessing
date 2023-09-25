# C0_text_preprocessing 
The module contains the function (*text_preprocessing*) that preprocesses the textual part of a Twitter post to make it a suitable input for the other modules, i.e., C0_topic_prediction and C2_moral_prediction.
Preprocessing steps are tailored to the needs of these two additional modules. Namely, given an input text (*text*), the function returns a dictionary of two items with *moral* and *topic* as keys, respectively, and the corresponding preprocessed texts as values.
The module contains a Flask app that performs the preprocessing steps for each task. 
A working example is reported in the *example.py* file. In the example, a Flask server is launched to listen on port *127.0.0.1:5000* and a request with the textual part of a tweet (*text*) is done. A message with the dictionary containing two different preprocessed versions of the input data (*moral* and *topic*) is received as an answer to the request.
