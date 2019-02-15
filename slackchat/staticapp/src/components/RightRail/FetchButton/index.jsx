import React from 'react';

import Loader from 'react-loader-spinner';

import styles from './styles.scss';

class FetchButton extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      processing: false,
    };
  }

  clickHandler = () => {
    this.props.onFeedback(null);
    this.setState({ processing: true });

    this.props.onClick().then(resp => {
      if (!resp.ok) {
        this.props.onFeedback(resp.statusText, true);
        this.setState({ processing: false });
      } else {
        return resp.json();
      }
    }).then(resp => {
      if (resp) {
        this.props.onFeedback(resp.text, false);
        this.setState({ processing: false });
        this.props.callback(resp);
      }
    });
  }

  render() {
    const { props } = this;
    return (
      <div className={styles.component}>
        <button onClick={this.clickHandler} {...props.buttonProps} disabled={props.buttonProps.disabled || this.state.processing}>
          <div className='button-text'>{props.children}</div>

          {this.state.processing &&
            <div className='button-icon button-loader'>
              <Loader
                className='test'
                type='Oval'
                color='#fff'
                width='15px'
                height='15px'
              />
            </div>
          }

        </button>
      </div>
    );
  }
}

FetchButton.defaultProps = {
  callback: () => null,
  onClick: () => null,
};

export default FetchButton;
