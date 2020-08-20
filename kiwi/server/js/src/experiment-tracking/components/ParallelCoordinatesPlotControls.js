import React from 'react';
import PropTypes from 'prop-types';
import { TreeSelect } from 'antd';
import { IconButton } from '../../common/components/IconButton';

export class ParallelCoordinatesPlotControls extends React.Component {
  static propTypes = {
    // An array of available parameter keys to select
    paramKeys: PropTypes.arrayOf(PropTypes.string).isRequired,
    // An array of available metric keys to select
    metricKeys: PropTypes.arrayOf(PropTypes.string).isRequired,
    selectedParamKeys: PropTypes.arrayOf(PropTypes.string).isRequired,
    selectedMetricKeys: PropTypes.arrayOf(PropTypes.string).isRequired,
    handleParamsSelectChange: PropTypes.func.isRequired,
    handleMetricsSelectChange: PropTypes.func.isRequired,
  };

  static handleFilterChange = (text, option) =>
    option.props.title.toUpperCase().includes(text.toUpperCase());

  render() {
    const {
      paramKeys,
      metricKeys,
      selectedParamKeys,
      selectedMetricKeys,
      handleParamsSelectChange,
      handleMetricsSelectChange,
    } = this.props;
    return (
      <div className='plot-controls'>
        <div>
          Parameters:
          <IconButton
            icon={<i className='far fa-minus-square' />}
            onClick={(e) => handleParamsSelectChange([])}
            style={{ marginLeft: '1em' }}
          />
        </div>
        <TreeSelect
          className='metrics-select'
          searchPlaceholder='Please select parameters'
          value={selectedParamKeys}
          showCheckedStrategy={TreeSelect.SHOW_PARENT}
          treeCheckable
          treeData={paramKeys.map((k) => ({ title: k, value: k, label: k }))}
          onChange={handleParamsSelectChange}
          filterTreeNode={ParallelCoordinatesPlotControls.handleFilterChange}
        />

        <div style={{ marginTop: 20 }}>Metrics:</div>
        <TreeSelect
          className='metrics-select'
          searchPlaceholder='Please select metrics'
          value={selectedMetricKeys}
          showCheckedStrategy={TreeSelect.SHOW_PARENT}
          treeCheckable
          treeData={metricKeys.map((k) => ({ title: k, value: k, label: k }))}
          onChange={handleMetricsSelectChange}
          filterTreeNode={ParallelCoordinatesPlotControls.handleFilterChange}
        />
      </div>
    );
  }
}
