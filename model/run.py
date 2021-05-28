import os
import sys
print(sys.path)
import pandas as pd
import numpy as np
import lightgbm as lgb
"""
===========================================================
# 以上为导入依赖包, 所需的依赖包请在requirements.txt中列明 
-----------------------------------------------------------
# 以下为选手自定义文件和代码
===========================================================
"""
origin_cols = ['receive_time',  'action_code', 'alarm_code', 'altitude',
       'auto_idling', 'avg_fuel_consumption', 'battery_voltage',
       'cooling_water_temperature', 'day_fuel_consumption',
       'displacement_direction', 'displacement_speed', 'engine_output_power',
       'engine_output_torque', 'engine_speed', 'fuel_level',
       'fuel_temperature', 'gear', 'hydraulic_oil_temperature',
       'intake_temperature', 'oil_pressure', 'pump1_current', 'pump1_flow',
       'pump1_pressure', 'pump2_current', 'pump2_flow', 'pump2_pressure',
       'pump_total_absorbed_power', 'pump_total_absorbed_torque',
       'realtime_fuel_consumption', 'total_idle_time', 'workmode']

def get_features(data):
    data = data.sort_values('receive_time')
    for f in ['action_code', 'alarm_code', 'auto_idling', 'workmode', 'intake_temperature', 'gear', 'fuel_temperature', 'displacement_speed']:
        data[f'{f}_nunique'] = data[f].nunique()
    
    data['count'] = len(data)
    for f in ['altitude', 'avg_fuel_consumption', 'cooling_water_temperature', 'battery_voltage', 'day_fuel_consumption', 'displacement_direction', 'engine_output_power', 'engine_speed',
             'fuel_level', 'hydraulic_oil_temperature', 'intake_temperature', 'oil_pressure', 'pump1_current', 'pump1_flow', 'pump1_pressure', 'pump_total_absorbed_power', 'pump_total_absorbed_torque',
              'realtime_fuel_consumption', 'total_idle_time'
             ]:
        data[f'{f}_max'] = data[f].max()
        data[f'{f}_mean'] = data[f].mean()
        data[f'{f}_min'] = data[f].min()
        data[f'{f}_std'] = data[f].std()
        data[f'{f}_skew'] = data[f].skew()
    return data.drop_duplicates('serial_no').drop(origin_cols, axis=1)



"""
===========================================================
# 选手自定义文件和代码到此为止
-----------------------------------------------------------
# 以下为main()入口函数，请谨慎修改
# main()函数必须包含to_pred_dir,result_save_path两个参数,其他参数
# 不做要求, 由选手自定义
===========================================================
"""
def main(to_pred_dir,result_save_path):
    """
        to_pred_path: 需要预测的文件夹路径
        to_save_path: 预测结果文件保存路径
    """
    # 需要预测的文件列表
    to_pred_file_list = [os.path.join(to_pred_dir,f) for f in os.listdir(to_pred_dir)]
    """
        本示例代码省略模型过程,且假设预测结果全为1
        选手代码需要自己构建模型，并通过模型预测结果
    """
    result = []
    predictions_lgb = np.zeros((len(to_pred_file_list)))
    data = None
    for path in to_pred_file_list:
        d = pd.read_csv(path)
        d = get_features(d)
        data = pd.concat([data, d])
    features = data.columns
    features = features.drop('serial_no')
    cwd = sys.argv[0]
    print(cwd)
    for i in range(5):
        clf = lgb.Booster(model_file=os.path.join(cwd[:-6], f'model_{i}.txt'))
        y_pred = clf.predict(data[features], num_iteration=clf.best_iteration)
        predictions_lgb[:] += y_pred / 5   
    y_pred = [1 if i >= 0.6 else 0 for i in predictions_lgb]
    data['label'] = y_pred
    data[['serial_no', 'label']].to_csv(result_save_path,index=None)
    

"""
===========================================================
# main()到此为止
-----------------------------------------------------------
# 以下代码不得修改, 若修改以下代码将会导致无法计算得分。
===========================================================
"""

if __name__ == "__main__":
    to_pred_dir = sys.argv[1]  # 所需预测的文件夹路径
    result_save_path = sys.argv[2]  # 预测结果保存文件路径
    main(to_pred_dir,result_save_path)
