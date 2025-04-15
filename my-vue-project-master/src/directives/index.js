import Vue from 'vue';

Vue.directive('dialogDrag', {
  bind(el) {
    const dialogHeaderEl = el.querySelector('.el-dialog__header');
    const dragDom = el.querySelector('.el-dialog');
    dialogHeaderEl.style.cursor = 'move';

    let isDown = false;
    let startX, startY, left, top;

    dialogHeaderEl.onmousedown = (e) => {
      isDown = true;
      startX = e.clientX - dragDom.offsetLeft;
      startY = e.clientY - dragDom.offsetTop;
      document.addEventListener('mousemove', onMouseMove);
      document.addEventListener('mouseup', onMouseUp);
    };

    const onMouseMove = (e) => {
      if (!isDown) return;
      left = e.clientX - startX;
      top = e.clientY - startY;
      dragDom.style.left = `${left}px`;
      dragDom.style.top = `${top}px`;
    };

    const onMouseUp = () => {
      isDown = false;
      document.removeEventListener('mousemove', onMouseMove);
      document.removeEventListener('mouseup', onMouseUp);
    };
  }
});