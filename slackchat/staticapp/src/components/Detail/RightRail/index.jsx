import React from 'react';
import Sticky from 'react-stickynode';
import Markdown from 'react-markdown';
import classnames from 'classnames';

import styles from './styles.scss';

class RightRail extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      feedback: null,
      error: false,
    };
  }

  onFeedback = (feedback, error) => {
    this.setState({ feedback, error });
  }

  render() {
    const { submit, statusText, statusLevel } = this.props;

    return (
      <Sticky enabled top={70} className={styles.component}>
        <button className={'btn btn-primary'} onClick={submit}>Save</button>

        <div className={classnames('feedback', statusLevel)}>
          <Markdown source={statusText} linkTarget='_blank' />
        </div>
      </Sticky>
    );
  }
}

export default RightRail;
