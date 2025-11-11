# app.py
import os
import glob
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__, template_folder='templates') # name of the .py


# A humble variable to be put in the web.
# It can be a hole folder or database in the future
current_text = "Web Test"
img_idx = 0

 # enable URL to include image index
def get_image_list(img_dir=os.path.join(app.root_path, 'static', 'images')):
    # image extensions
    supported_extensions = ['*.jpg', '*.jpeg', '*.png', '*.gif'] 
    image_files = []
    for ext in supported_extensions:
        # 'path/to/static/images/*(extension)'
        search_pattern = os.path.join(img_dir, ext)
        
        # glob.glob() returns the whole matched addresses
        full_paths = glob.glob(search_pattern)
        
        # take only the file name of entire sddress using os.path.basename()
        filenames = [os.path.basename(path) for path in full_paths]
        image_files.extend(filenames) # extend() makes all elements in a iterable append to the list one by one
        
    image_files.sort()
    
    return image_files

global image_list
image_list=get_image_list()
@app.route('/', methods=['GET', 'POST'])
# @app.route('/<int:img_list>', methods=['GET'])
def gallery():
    global current_text
    global img_idx
    # submit processing list (POST request)
    if request.method == 'POST':
        # Get a column call 'new_content' from the processing list
        new_content = request.form.get('new_content') # get the text inside textarea  
        if new_content:
            # update the content of the global variable (the editable string)
            current_text = new_content
            # redirect GET request to avoid user submit multiple times after refreshing the page
            return redirect(url_for('gallery')) #
        # Get a column call 'action' from the processing list
        action = request.form.get('action') # check whether user pick 'previous/next' image
        # update idx based on buttons
        if action == 'next':
            img_idx = (img_idx + 1) % len(image_list) # using % to avoid index exceeding amount of images
        elif action == 'prev':
            img_idx = (img_idx - 1) % len(image_list)
            if img_idx < 0: # hitting prev button while on the last image
                img_idx = len(image_list) - 1
        else:
            img_idx = img_idx
        return redirect(url_for('gallery'))
    # process display of the web (GET request) and implement the changes
    return render_template('index.html', content=current_text, current_image_name=image_list[img_idx],
                            current_index=img_idx, total_images=len(image_list))




if __name__ == '__main__':
    # activate Flask app.
    image_folder = os.path.join(app.root_path, 'static', 'images')
    app.run(debug=True) 
    # Setting debug to be Ture so that server is auto-reload once code is changed, just for convenience

