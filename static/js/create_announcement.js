const initialData = {
  name: "Title",
  about: [
    {
      insert: "Sample Announcement body.\n",
    },
  ],
};

var quill;
window.onload = function () {
  quill = new Quill("#quillEditor", {
    modules: {
      toolbar: [
        ["bold", "italic"],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
    },
    theme: "snow",
  });

  reset_btn = document.getElementById("resetForm");
  reset_btn.onclick = resetForm;

  form = document.getElementById("createAnnouncementForm");
  form.addEventListener("formdata", (event) => {
    data = document.getElementsByClassName("ql-editor")[0].innerHTML;
    event.formData.append("body", data);
  });

  resetForm();
};

function resetForm() {
  document.querySelector('[name="title"]').value = initialData.name;
  document.querySelector('[name="date_from"]').value = "";
  document.querySelector('[name="date_to"]').value = "";
  quill.setContents(initialData.about);
}
