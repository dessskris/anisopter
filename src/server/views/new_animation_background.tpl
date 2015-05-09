<!DOCTYPE html>
<html>
% include('head.tpl', title="Upload Animation Background")
<body>
% include('header.tpl')
<div class="container">
    <h2>Upload Animation Background</h2>
    <form action="/target_animation/background/upload"
          method="post"
          enctype="multipart/form-data">
        <div class="form-group">
            <label for="upload">File Input</label>
            <input type="file" id="upload" name="upload"
                   accept="image/png, image/jpeg">
            <p class="help-block">
                Upload a file to use as a background for your animations.
            </p>
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
    </form>
</div>
</body>
</html>