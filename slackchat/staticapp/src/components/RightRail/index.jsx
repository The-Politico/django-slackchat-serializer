import React from 'react';
import Sticky from 'react-stickynode';
import classnames from 'classnames';

import FetchButton from './FetchButton';

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
    const { props } = this;
    const saveButtonData = {
      disabled: !props.changed,
      className: classnames('btn btn-primary', {
        disabled: !props.changed,
      }),
      title: !props.changed ? 'Make changes to save' : '',
    };

    const webhookButtonData = {
      disabled: props.changed,
      className: classnames('btn btn-primary', {
        disabled: props.changed,
      }),
      title: props.changed ? 'Save changes before action' : '',
    };

    return (
      <Sticky enabled top={70} className={styles.component}>
        <h3>Actions</h3>
        <FetchButton buttonProps={saveButtonData} onClick={props.save} callback={props.saveCallback} onFeedback={this.onFeedback}>Save To Draft</FetchButton>
        <FetchButton buttonProps={webhookButtonData} onClick={props.update} onFeedback={this.onFeedback}>Save & Publish</FetchButton>
        <FetchButton buttonProps={webhookButtonData} onClick={props.rebake} onFeedback={this.onFeedback}>Rebake</FetchButton>
        <p className={classnames('feedback', { error: this.state.error })}>{this.state.feedback}</p>
      </Sticky>
    );
  }
}

export default RightRail;
