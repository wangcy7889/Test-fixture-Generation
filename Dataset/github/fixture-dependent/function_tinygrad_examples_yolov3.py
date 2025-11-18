import numpy as np
from tinygrad.helpers import fetch

def show_labels(prediction, confidence=0.5, num_classes=80):
    coco_labels = fetch('https://raw.githubusercontent.com/pjreddie/darknet/master/data/coco.names').read_bytes()
    coco_labels = coco_labels.decode('utf-8').split('\n')
    prediction = prediction.detach().numpy()
    conf_mask = prediction[:, :, 4] > confidence
    prediction *= np.expand_dims(conf_mask, 2)
    labels = []
    for img_pred in prediction:
        max_conf = np.amax(img_pred[:, 5:5 + num_classes], axis=1)
        max_conf_score = np.argmax(img_pred[:, 5:5 + num_classes], axis=1)
        max_conf_score = np.expand_dims(max_conf_score, axis=1)
        max_conf = np.expand_dims(max_conf, axis=1)
        seq = (img_pred[:, :5], max_conf, max_conf_score)
        image_pred = np.concatenate(seq, axis=1)
        non_zero_ind = np.nonzero(image_pred[:, 4])[0]
        assert all(image_pred[non_zero_ind, 0] > 0)
        image_pred_ = np.reshape(image_pred[np.squeeze(non_zero_ind), :], (-1, 7))
        classes, indexes = np.unique(image_pred_[:, -1], return_index=True)
        for index, coco_class in enumerate(classes):
            label, probability = (coco_labels[int(coco_class)], image_pred_[indexes[index]][4] * 100)
            print(f'Detected {label} {probability:.2f}')
            labels.append(label)
    return labels