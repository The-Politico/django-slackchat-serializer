import React from 'react';
import Form from 'react-jsonschema-form';
import assign from 'lodash/assign';

import prepData from 'Utils/detail/prepData';
import generateSchema from 'Utils/detail/generateSchema';
import generateStatus from 'Utils/detail/generateStatus';
import { cms } from 'Utils/detail/api';

import * as status from 'Content/detail/status';

import widgets from './widgets';
import RightRail from './RightRail';

import styles from './styles.scss';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = assign(
      {},
      generateStatus(props.data),
      {
        data: props.data,
        schema: generateSchema(props.data),
      });

    this.form = React.createRef();
  }

  save = () => {
    const page = this.props.page;
    const newPage = page === 'new';

    const data = prepData(this.state.data, newPage);

    let request;
    if (page === 'new') {
      request = cms.POST(data);
    } else {
      request = cms.PATCH(data);
    }

    request.then(resp => {
      this.onSave(resp);
    }).catch(err =>
      this.setState(status.error.generic(err))
    );
  }

  onSave = resp => resp.json().then(data => {
    if (!resp.ok) {
      this.setState(status.error.server(data.detail));
    } else {
      this.saveCallback(data);
    }
  }).catch(err => {
    console.error(err);
    this.setState(status.error.generic(resp.statusText));
  });

  saveCallback = resp => {
    if (resp.method === 'PATCH') {
      window.location.href = '../../';
    } else {
      window.location.href = '../';
    }
  }

  onFormChange = ({ formData }) => {
    this.setState(prev => {
      const data = assign({}, formData);
      if (prev.data.chat_type !== data.chat_type) {
        data.extras = {};
      }

      const newStatus = generateStatus(data);

      return assign({}, {
        data,
        schema: generateSchema(data),
      },
      newStatus
      );
    });
  }

  onSubmit = arg => {
    // proxy for submission is complete
    if (!Array.isArray(arg)) {
      this.save();
    }
  }

  submit = () => {
    this.form.current.submit();
  }

  render() {
    const { data, schema, statusText, statusLevel } = this.state;

    return (
      <div className={styles.component + ' detail-container'}>
        <article className='cms-detail container'>
          <h1>{data.title ? data.title : 'Slack Chat'}</h1>
          <div className='row'>
            <div className='center-well col-9'>
              <Form
                schema={schema.json}
                uiSchema={schema.ui}
                formData={data}
                widgets={widgets}
                ref={this.form}
                onChange={this.onFormChange}
                onSubmit={this.onSubmit}
              >
                <div />
              </Form>
            </div>
            <div className='right-rail col-3'>
              <RightRail
                statusText={statusText}
                statusLevel={statusLevel}
                isPublished={data.published}
                submit={this.submit}
                callback={this.saveCallback}
              />
            </div>
          </div>
        </article>
      </div>
    );
  }
}

export default App;
