import assign from 'lodash/assign';
import baseSchema from './baseSchema';

class DetailForm {
  constructor(data) {
    this.state = {
      data: {},
      enums: [],
      customs: [],
    };
  }

  update(data) {
    this.state.data = assign({}, this.state.data, data);
    this.state.json = assign({}, this.state.json, baseSchema.json(data));
    this.state.ui = assign({}, this.state.ui, baseSchema.ui(data));
  }

  enum(key, values) {
    this.state.enums = [...this.state.enums, { key, values }];
  }

  register(name, schema) {
    this.state.customs = [...this.state.customs, { name, schema }];
  }

  render() {
    const { data, enums, customs } = this.state;

    const output = assign({}, {
      json: baseSchema.json(data),
      ui: baseSchema.ui(data),
    });

    enums.forEach(({ key, values }) => {
      output.json.properties[key].enum = values.map(v => v.value);
      output.json.properties[key].enumNames = values.map(v => v.label);
    });

    customs.forEach(({ name, schema }) => {
      output.json.properties[name] = schema.jsonSchema;
      output.ui[name] = schema.uiSchema;
    });

    return output;
  }
}

export default DetailForm;
