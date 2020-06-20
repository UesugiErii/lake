# Read tensor data from tensorboard file

# https://stackoverflow.com/questions/41074688/how-do-you-read-tensorboard-files-programmatically

from tensorboard.backend.event_processing import event_accumulator

ea = event_accumulator.EventAccumulator(
    file_path,
    size_guidance={event_accumulator.TENSORS: 0, event_accumulator.SCALARS: 0, }  # 0 means load all data
)  # see other use dir(event_accumulator)

"""
size_guidance: Information on how much data the EventAccumulator should
  store in memory. The DEFAULT_SIZE_GUIDANCE tries not to store too much
  so as to avoid OOMing the client. The size_guidance should be a map
  from a `tagType` string to an integer representing the number of
  items to keep per tag for items of that `tagType`. If the size is 0,
  all events are stored.
"""

ea.Reload()  # loads events from file
ea.Tags()

ea.Tensors('H')

ea.Tensors('H')[0].step  # return first record step

t = ea.Tensors('H')[0].tensor_proto.tensor_content
d = ea.Tensors('H')[0].tensor_proto.dtype
float(tf.io.decode_raw(t, d))
