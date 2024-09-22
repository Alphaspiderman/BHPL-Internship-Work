const initialData = {
  name: "Sample Title",
  about: [
    {
      insert: "Sample Announcement body.\n",
    },
  ],
};

var quill;
$(document).ready(function () {
  quill = new Quill("#quillEditor", {
    // modules: {
    //   toolbar: [
    //     ["bold", "italic"],
    //     [{ list: "ordered" }, { list: "bullet" }],
    //   ],
    // },
    theme: "snow",
  });

  reset_btn = document.getElementById("resetForm");
  reset_btn.onclick = resetForm;

  $("#createAnnouncementForm").submit(function (e) {
    e.preventDefault();
    submit_form();
  });

  resetForm();
});

function submit_form() {
  body = quill.getSemanticHTML();
  dateFrom = document.querySelector("#dateFrom").value;
  dateTo = document.querySelector("#dateTo").value;
  title = document.querySelector("#title").value;
  asAdmin = document.querySelector("#asAdmin").checked;
  file = document.querySelector("#formFile").files[0];

  formData = new FormData();

  formData.append("title", title);
  formData.append("body", body);
  formData.append("date_from", dateFrom);
  formData.append("date_to", dateTo);
  formData.append("as_admin", asAdmin);
  formData.append("file", file);

  $.ajax({
    type: "POST",
    url: "/api/announcements/new",
    data: formData,
    processData: false,
    contentType: false,
    success: function (data) {
      console.log(data);
      if (data.success) {
        alert("Announcement created successfully");
        resetForm();
      } else {
        alert(data.message);
      }
    },
    error: function (data) {
      console.log(data);
    },
  });
}

function resetForm() {
  data = quill.getSemanticHTML();
  document.querySelector("#title").value = initialData.name;
  document.querySelector("#dateFrom").value = "";
  document.querySelector("#dateTo").value = "";
  quill.setContents(initialData.about);
}
