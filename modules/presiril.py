from pysiril.siril import *
from pysiril.wrapper import *


# ==============================================================================
# EXAMPLE OSC_Processing with functions wrapper
# ==============================================================================

# 1. defining command blocks for creating masters and processing lights
def master_bias(bias_dir, process_dir):
    cmd.cd(bias_dir)
    cmd.convert('bias', out=process_dir, fitseq=True)
    cmd.cd(process_dir)
    cmd.stack('bias', type='rej', sigma_low=3, sigma_high=3, norm='no')


def master_flat(flat_dir, process_dir):
    cmd.cd(flat_dir)
    cmd.convert('flat', out=process_dir, fitseq=True)
    cmd.cd(process_dir)
    cmd.preprocess('flat', bias='bias_stacked')
    cmd.stack('pp_flat', type='rej', sigma_low=3, sigma_high=3, norm='mul')


def master_dark(dark_dir, process_dir):
    cmd.cd(dark_dir)
    cmd.convert('dark', out=process_dir, fitseq=True)
    cmd.cd(process_dir)
    cmd.stack('dark', type='rej', sigma_low=3, sigma_high=3, norm='no')


def light(light_dir, process_dir):
    cmd.cd(light_dir)
    cmd.convert('light', out=process_dir, fitseq=True)
    cmd.cd(process_dir)
    cmd.preprocess('light', dark='dark_stacked', flat='pp_flat_stacked', cfa=True, equalize_cfa=True, debayer=True)
    cmd.register('pp_light')
    cmd.stack('r_pp_light', type='rej', sigma_low=3, sigma_high=3, norm='addscale', output_norm=True, out='../result')
    cmd.close()


# ==============================================================================
# 2. Starting pySiril
app = Siril()
cmd = Wrapper(app)  # 2. its wrapper


def process(workdir):
    """
    Process the astro-photos in siril
    """

    try:

        app.Open()  # 2. ...and finally Siril

        # 3. Set preferences
        process_dir = './process'
        cmd.set16bits()
        cmd.setext('fit')

        # 4. Prepare master frames
        master_bias(workdir + '/biases', process_dir)
        master_flat(workdir + '/flats', process_dir)
        master_dark(workdir + '/darks', process_dir)

        # 5. Calibrate the light frames, register and stack them
        light(workdir + '/lights', process_dir)

    except Exception as e:
        print("\n**** ERROR *** " + str(e) + "\n")

    # 6. Closing Siril and deleting Siril instance
    app.Close()
    del app
