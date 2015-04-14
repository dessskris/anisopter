<!DOCTYPE html>
<html>
% include('head.tpl', title="Animation")
<body>
% include('header.tpl')
<div class="container">
    <h2>General</h2>
    <table class="table">
        <tr>
            <td>Animation ID</td>
            <td>{{animation['_id']}}</td>
        </tr>
        <tr>
            <td>Description</td>
            <td>{{animation['description']}}</td>
        </tr>
        <tr>
            <td>Number of Targets</td>
            <td>{{len(animation['targets'])}}</td>
        </tr>
        <tr>
            <td>Width</td>
            <td>{{animation['width']}}</td>
        </tr>
        <tr>
            <td>Height</td>
            <td>{{animation['height']}}</td>
        </tr>
        <tr>
            <td>Duration</td>
            <td>{{animation['duration']}} ms</td>
        </tr>
    </table>
</div>
</body>
</html>