import React from 'react';
import Sticky from 'react-stickynode';

import styles from './styles.scss';

const RightRail = (props) => (
  <Sticky enabled top={70} className={styles.component}>
    <a href='./new'>
      <button className={'btn btn-primary'}>New Chat</button>
    </a>
  </Sticky>
);

export default RightRail;
