
$(document).ready(function(){
    $('#upload_button').click(function() {
        $('#spinner').show();
    });
});

function useDefaultValues(){
        document.getElementById('invert').value = "True";
        document.getElementById('diameter').value = 21;
        document.getElementById('minmass').value = 2600;
        document.getElementById('noise_size').value = 4;
        document.getElementById('separation').value = 25;
        document.getElementById('smoothing_size').value = 21;
    }
