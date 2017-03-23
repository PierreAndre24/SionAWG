class MultiDimExperiment():
    def __init__(self):

        # File information
        self.FileInfo = {}
        # self.fileversion = 0
        # self.filepath = ''
        # self.filename = ''
        # self.filetype = ''

        # Experimental data only
        # This is a dataset that stores everything that comes out of the experiment
        self.ExperimentalData = {}
        self.ExperimentalData['dimensions'] = [0]

        # Experiment Parameters
        # This is a group of datasets that stores everything that comes in the experiment
        # It always includes a key 'Info', which is a dictionary.
        # Grouping all setup parameters (measurement speed, Rampmode, ...) in
        # 'Info' allows a simpler saving/reading
        self.ExperimentalParameters = {}
        self.ExperimentalParameters['Info'] = {}
