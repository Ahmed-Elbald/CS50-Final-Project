document.addEventListener('DOMContentLoaded', function () {
  dialog_btns = document.querySelectorAll('.open-modal');
  for (let i = 0; i < dialog_btns.length; i++) {
    dialog_btns[i].addEventListener('click', function() {
      modal = dialog_btns[i].nextElementSibling;
      modal.showModal();
      close_modal = modal.lastElementChild;
      close_modal.addEventListener('click', function() {
        modal.close();
      });
    });
  };
});