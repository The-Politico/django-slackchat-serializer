import React from 'react';

const BooleanField = (props) => {
  if (props.active) {
    return <p><a target='_blank' href={props.href + '/'}>{props.children}</a> <span className='emoji' role='img' aria-label='yes'>✅</span></p>;
  } else {
    return <p>{props.children} <span className='emoji' role='img' aria-label='no'>❌</span></p>;
  }
};

export default BooleanField;
