import assign from 'lodash/assign';
import baseSchema from 'Content/baseSchema';

class DetailForm {
  constructor(data) {
    console.log('base', baseSchema.json);

    this.state = {
      data: {},
      json: assign({}, baseSchema.json),
      ui: assign({}, baseSchema.ui),
    };
  }

  update(data) {
    this.state.data = assign({}, this.state.data, data);
  }

  enum(key, values) {
    this.state.json.properties[key].enum = values.map(v => v.value);
    this.state.json.properties[key].enumNames = values.map(v => v.label);
  }

  register(name, schema) {
    this.state.json.properties[name] = schema.jsonSchema;
    this.state.ui[name] = schema.uiSchema;
  }

  render() {
    return {
      json: this.state.json,
      ui: this.state.ui,
    };
  }
}

export default DetailForm;
