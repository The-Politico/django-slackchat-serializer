import React from 'react';

import { Sketch } from 'politico-style';
import ChatItem from './ChatItem';
import RightRail from './RightRail';

import styles from './styles.scss';

class App extends React.Component {
  render() {
    return (
      <div className={styles.component + ' list-container'}>
        <article className='cms-list container'>
          <Sketch.Header title='Slack Chat'></Sketch.Header>

          <div className='row'>
            <div className='center-well col-9'>
              {this.props.data.map(i =>
                <ChatItem key={i.id} {...i} />
              )}
            </div>
            <div className='right-rail col-3'>
              <RightRail />
            </div>
          </div>

        </article>
      </div>
    );
  }
}

export default App;
