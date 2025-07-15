$(function () {
  // Load departments
  $.getJSON('/departments.php', function (data) {
    let $sel = $('#department');
    data.departments.forEach(function (d) {
      $sel.append(`<option value="${d.id}">${d.name}</option>`);
    });
  });

  // Submit form
  $('#enquiryForm').on('submit', function (e) {
    e.preventDefault();
   alertBox('Sub', 'danger')
    
    $('#submitBtn').prop('disabled', true);

    $.ajax({
      url: '/save_enquiry.php',
      method: 'POST',
      data: $(this).serialize(),
      dataType: 'json',
      success: function (resp) {
        if (resp.status === 'success' || resp.result === 'success') {
          alertBox('Your enquiry has been submitted successfully!', 'success');
          $('#enquiryForm')[0].reset();
        } else {
          alertBox('Submission failed. Please try again.', 'danger');
        }
      },
      error: function () {
        alertBox('Server error. Please try later.', 'danger');
      },
      complete: function () {
        $('#submitBtn').prop('disabled', false);
      }
    });
  });

  function alertBox(msg, type) {
    $('#alertPlaceholder').html(`
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${msg}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    `);
  }
});
