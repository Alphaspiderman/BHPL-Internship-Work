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
  $(".input-group.date").datepicker({ format: "yyyy-mm-dd" });
  quill = new Quill("#quillEditor", {
    modules: {
      toolbar: [
        ["bold", "italic"],
        [{ list: "ordered" }, { list: "bullet" }],
      ],
    },
    theme: "snow",
  });

  function resetForm() {
    document.querySelector('[name="title"]').value = initialData.name;
    quill.setContents(initialData.about);
  }

  const form = document.querySelector("form");
  form.addEventListener("formdata", (event) => {
    data = document.getElementsByClassName("ql-editor")[0].innerHTML;
    // Append Quill content before submitting
    console.log(data);
    event.formData.append("body", data);
  });

  document.querySelector("#resetForm").addEventListener("click", () => {
    resetForm();
  });

  resetForm();
};
