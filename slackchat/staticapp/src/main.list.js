import React from 'react';
import ReactDOM from 'react-dom';
import App from 'Components/List';

import './theme/base.scss';

const props = {
  data: window.DATA,
};

ReactDOM.render(
  <App {...props} />,
  document.getElementById('app')
);
