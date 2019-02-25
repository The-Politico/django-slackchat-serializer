import React from 'react';

import BaseToggle from './Base';

const Toggle = (props) => {
  return (
    <BaseToggle
      active={props.value}
      required={props.required}
      onClick={(value) => props.onChange(value)}
    />
  );
};

export default Toggle;
