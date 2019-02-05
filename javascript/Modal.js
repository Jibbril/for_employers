// Small script implementng a modal for a website. Meant to be called from 
// a user clicking the menu icon on a website.

import $ from 'jquery';

class Modal {
  //Opens a modal, side menu on large screen, full screen on small

  constructor() {
    this.body = $('body');
    this.topNavOpenButton = $(".contact-modal__open-top-nav");
    this.footerOpenButton = $(".site-footer__contact-banner");
    this.modal = $(".contact-modal");
    this.closeModalButton = $(".contact-modal__close-button");
    this.events();
  }

  events() {
    //Clicking open modal button
    this.topNavOpenButton.click(this.openModal.bind(this));
    this.footerOpenButton.click(this.openModal.bind(this));

    //clicking the x close modal button
    this.closeModalButton.click(this.closeModal.bind(this));

    //pushes the escape key
    $(document).keyup(this.keyPressHandler.bind(this));
  }

  keyPressHandler(e) {
    if (e.keyCode == 27) {
      this.closeModal();
    }
  }

  openModal() {
    this.modal.addClass("contact-modal--is-visible");
    console.log($(window).width())
    if ($(window).width() < 900) {
      this.body.addClass('body--overflow-hidden');
    }
    return false;
  }

  closeModal() {
    this.modal.removeClass("contact-modal--is-visible");
    this.body.removeClass('body--overflow-hidden');
    return false;
  }
}

export default Modal;
