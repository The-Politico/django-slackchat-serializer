import React from 'react';
import Form from 'react-jsonschema-form';

import dataHasChanged from 'Utils/dataHasChanged';
import prepData from 'Utils/prepData';
import generateScheme from 'Utils/generateScheme';
import api, { POST, PATCH } from 'Utils/api';

import widgets from './widgets';
import RightRail from './RightRail';

class App extends React.Component {
  constructor(props) {
    super(props);

    const chatType = props.chatTypeLookup[props.data.chat_type];

    this.state = {
      chatType,
      data: props.data,
      schema: generateScheme(chatType),
      changed: false,
    };

    this.form = React.createRef();
  }

  save = () => {
    const page = this.props.page;
    const newPage = page === 'new';

    const data = prepData(this.state.data, newPage);

    if (page === 'new') {
      return api(POST, data);
    } else {
      return api(PATCH, data);
    }
  }

  saveCallback = resp => {
    if (resp.method === 'PATCH') {
      window.location.reload();
    }
  }

  onFormChange = ({ formData }) => {
    this.setState({
      data: formData,
      changed: dataHasChanged(window.CHAT_DATA, formData),
      schema: generateScheme(this.props.chatTypeLookup[formData.chat_type]),
    });
  }

  render() {
    const { props, state } = this;

    return (
      <article className='cms-detail container'>
        <div className='row'>
          <div className='center-well col-9'>
            <Form
              schema={state.schema.json}
              uiSchema={state.schema.ui}
              formData={this.state.data}
              widgets={widgets}
              ref={this.form}
              onChange={this.onFormChange}
            >
              <div />
            </Form>
          </div>
          <div className='right-rail col-3'>
            <RightRail
              save={this.save}
              saveCallback={this.saveCallback}
              changed={this.state.changed}
            />
          </div>
        </div>
      </article>
    );
  }
}

export default App;
