import scipy.io as sio

def get_pose_params_from_mat(mat_path):
    mat = sio.loadmat(mat_path)
    pre_pose_params = mat['Pose_Para'][0]
    pose_params = pre_pose_params[:5]
    return pose_params