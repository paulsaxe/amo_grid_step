# -*- coding: utf-8 -*-
"""Non-graphical part of the AMO Grid step in a MolSSI workflow

In addition to the normal logger, two logger-like printing facilities are
defined: 'job' and 'printer'. 'job' send output to the main job.out file for
the job, and should be used very sparingly, typically to echo what this step
will do in the initial summary of the job.

'printer' sends output to the file 'step.out' in this steps working
directory, and is used for all normal output from this step.
"""

import json
import logging
import molssi_workflow
from molssi_workflow import ureg, Q_, data    # noqa F401
import molssi_util.printing as printing
from molssi_util.printing import FormattedText as __
import os.path

import amo_grid_step

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter('amo_grid')


class AMOGrid(molssi_workflow.Node):
    def __init__(self,
                 workflow=None,
                 title='AMO Grid',
                 extension=None):
        """An AMO Grid step in a MolSSI flowchart.

        You may wish to change the title above, which is the string displayed
        in the box representing the step in the flowchart.

        Keyword arguments:
        """
        logger.debug('Creating AMO Grid {}'.format(self))

        super().__init__(
            workflow=workflow,
            title='AMO Grid',
            extension=extension)

        self.parameters = amo_grid_step.AMOGridParameters()

    def description_text(self, P):
        """Create the text description of what this step will do.
        The dictionary of control values is passed in as P so that
        the code can test values, etc.
        """

        text = (
            'Generate a grid for a scattering calculation. The central grid '
            'has an l-max of {central grid lmax} using a '
            '{central grid angular quadrature} quadrature for the angular '
            'portion, with '
        )
        if P['central grid angular quadrature'] == 'Lebedev':
            text += 'Lebedev rule {central grid Lebedev rule}.'
        elif (P['central grid angular quadrature'] == 'Gauss' or
              P['central grid angular quadrature'] == 'mixed'):
            text += (
                'a {central grid phi quadrature} quadrature for phi using '
                '{central grid phi n-points} points and a '
                '{central grid theta quadrature} quadrature for theta using '
                '{central grid theta n-points} points.'
            )
        else:
            text += (
                'Lebedev rule {central grid Lebedev rule} or a'
                'a {central grid phi quadrature} quadrature for phi using '
                '{central grid phi n-points} points and a '
                '{central grid theta quadrature} quadrature for theta using '
                '{central grid theta n-points} points, depending on the method'
                ' used at runtime.'
            )
        text += (
            ' The radial portion of the grid uses a '
            '{central grid radial quadrature} quadrature, divided into '
        )
        tmp = P['central grid region n-points']
        if tmp[0] == "$":
            n = 'unknown number of'
        else:
            # n = len(json.loads(tmp.replace("'", '"')))
            n = len(tmp)
            
        text += '{} regions.'.format(n)

        text += '\n\n'
        text += (
            'The grid on each atom '
            'has an l-max of {atomic grid lmax} using a '
            '{atomic grid angular quadrature} for the angular portion, with '
        )
        if P['atomic grid angular quadrature'] == 'Lebedev':
            text += 'Lebedev rule {atomic grid Lebedev rule}.'
        elif (P['atomic grid angular quadrature'] == 'Gauss' or
              P['atomic grid angular quadrature'] == 'mixed'):
            text += (
                'a {atomic grid phi quadrature} quadrature for phi using '
                '{atomic grid phi n-points} points and a '
                '{atomic grid theta quadrature} quadrature for theta using '
                '{atomic grid theta n-points} points.'
            )
        else:
            text += (
                'Lebedev rule {atomic grid Lebedev rule} or a'
                'a {atomic grid phi quadrature} quadrature for phi using '
                '{atomic grid phi n-points} points and a '
                '{atomic grid theta quadrature} quadrature for theta using '
                '{atomic grid theta n-points} points, depending on the method'
                ' used at runtime.'
            )
        n = P['atomic grid region n-points'][0]
        r = P['atomic grid region outer limit'][0]
        text += (
            ' The radial portion of the grid uses a '
            '{atomic grid radial quadrature} quadrature with '
        )
        text += ('{} points extending to {} from the atom.'.format(n, r))
                 
        return text

    def run(self):
        """Run a AMO Grid step.
        """

        next_node = super().run(printer=printer)

        input = self.get_input()
        printer.important(input)

        filename = os.path.join(self.directory, 'input.in')
        with open(filename, 'w') as fd:
            fd.write(input)

        files = {'input.in': input}
        local = molssi_workflow.ExecLocal()
        return_files = ['output.dat']
        result = local.run(
            cmd=['amo_grid', 'input.in'],  # nopep8
            files=files,
            return_files=return_files)

        # Figure out what happened
        if result['stderr'] != '':
            logger.warning('stderr:\n' + result['stderr'])
            with open(os.path.join(self.directory, 'stderr.txt'),
                      mode='w') as fd:
                fd.write(result['stderr'])

        for filename in result['files']:
            with open(os.path.join(self.directory, filename), mode='w') as fd:
                if result[filename]['data'] is not None:
                    fd.write(result[filename]['data'])
                else:
                    fd.write(result[filename]['exception'])

        # Analyze the results
        self.analyze()

        return next_node

    def get_input(self):
        """Returns the input for the grid program
        """
        if data.structure is None:
            logger.error('AMOGrid get_input(): there is no structure!')
            raise RuntimeError('AMOGrid get_input(): there is no structure!')

        atoms = data.structure['atoms']
        n_atoms = len(atoms['elements'])

        P = self.parameters.current_values_to_dict(
            context=molssi_workflow.workflow_variables._data
        )

        lines = []
        lines.append('[DEFAULTS]')
        lines.append('{:>21s} = {}'.format('number_of_atoms', n_atoms))
        lines.append(
            '{:>21s} = {}'
            .format('r_type_quadrature',
                    P['central grid radial quadrature'].lower())
        )
        lines.append(
            '{:>21s} = {}'
            .format('angular_quad_type',
                    P['central grid angular quadrature'].lower()))
        lines.append('')
        lines.append('## central grid ##')
        lines.append('')
        lines.append('[center]')
        # lines.append('{:>21s} = {}'
        #              .format('r_type_quadrature',
        #                      P['central grid radial quadrature']))

        # regions
        npoints = P['central grid region n-points']
        limits = P['central grid region outer limit']
        lines.append('{:>21s} = {}'.format('region_num', len(npoints)))
        lines.append('{:>21s} = {}'.format('r_origin_fixed', 0))
        lines.append('{:>21s} = {}'.format('r_endpt_fixed', 1))
        line = '{:>21s} = {}'.format('r_intervals', '0.0')
        for r in limits:
            line += ', {}'.format(r)
        lines.append(line)
        line = '{:>21s} = {}'.format('r_num_shell_pts', npoints[0])
        for n in npoints[1:]:
            line += ', {}'.format(n)
        lines.append(line)

        lines.append('')
        lines.append('{:>21s} = {}'
                     .format('cent_lmax', P['central grid lmax']))
        # lines.append('{:>21s} = {}'.format(
        #     'angular_quad_type', P['central grid angular quadrature']))
        if P['central grid angular quadrature'] == 'Lebedev':
            lines.append('{:>21s} = {}'.format(
                'lebedev_rule', P['central grid Lebedev rule']))
        else:
            lines.append('{:>21s} = {}'.format(
                'phi_type_quadrature', P['central grid phi quadrature']))
            lines.append('{:>21s} = {}'.format(
                'phi_quadrature_size', P['central grid phi n-points']))
            lines.append('{:>21s} = {}'
                         .format('theta_type_quadrature',
                                 P['central grid theta quadrature']).lower()
            )
            lines.append('{:>21s} = {}'.format(
                'theta_quadrature_size', P['central grid theta n-points']))

        # And the grids for the atoms
        lines.append('')
        lines.append('## Atom-centered grids ##')

        # Center the atoms on 0
        cx = 0.0
        cy = 0.0
        cz = 0.0
        for x, y, z in atoms['coordinates']:
            cx += x
            cy += y
            cz += z
        cx /= n_atoms
        cy /= n_atoms
        cz /= n_atoms

        i = 0
        for element, xyz in zip(atoms['elements'], atoms['coordinates']):
            i += 1
            x, y, z = xyz
            lines.append('')
            lines.append('## atom {}: {} ##'.format(i, element))
            lines.append('[atom_{}]'.format(i))
            lines.append('{:>21s} = {}, {}, {}'
                         .format('atom_center', x-cx, y-cy, z-cz))
            lines.append(
                '{:>21s} = {}'
                .format('r_type_quadrature',
                        P['atomic grid radial quadrature'].lower())
            )

            # regions
            npoints = P['atomic grid region n-points']
            limits = P['atomic grid region outer limit']
            if not isinstance(npoints, list):
                npoints = [npoints]
            if not isinstance(limits, list):
                limits = [limits]
            lines.append('{:>21s} = {}'.format('region_num', len(npoints)))
            lines.append('{:>21s} = {}'.format('r_origin_fixed', 0))
            lines.append('{:>21s} = {}'.format('r_endpt_fixed', 1))
            line = '{:>21s} = {}'.format('r_intervals', '0.0')
            for r in limits:
                line += ', {}'.format(r)
            lines.append(line)
            line = '{:>21s} = {}'.format('r_num_shell_pts', int(npoints[0]))
            for n in npoints[1:]:
                line += ', {}'.format(int(n))
            lines.append(line)

            lines.append('')
            lines.append('{:>21s} = {}'.format('lmax', P['atomic grid lmax']))
            lines.append('{:>21s} = {}'.format(
                'angular_quad_type', P['atomic grid angular quadrature']))
            # if P['atomic grid angular quadrature'] == 'Lebedev':
            if P['central grid angular quadrature'] == 'Lebedev':
                lines.append('{:>21s} = {}'.format(
                    'lebedev_rule', P['atomic grid Lebedev rule']))
            else:
                lines.append('{:>21s} = {}'.format(
                    'phi_type_quadrature', P['atomic grid phi quadrature']))
                lines.append('{:>21s} = {}'.format(
                    'phi_quadrature_size', P['atomic grid phi n-points']))
                lines.append('{:>21s} = {}'.format(
                    'theta_type_quadrature',
                    P['atomic grid theta quadrature']).lower()
                )
                lines.append('{:>21s} = {}'.format(
                    'theta_quadrature_size', P['atomic grid theta n-points']))

        return '\n'.join(lines)

    def analyze(self, indent='', **kwargs):
        """Do any analysis needed for this step, and print important results
        to the local step.out file using 'printer'
        """

        filename = 'output.dat'
        with open(os.path.join(self.directory, filename), mode='r') as fd:
            lines = fd.read().splitlines()

        data = {}
        test = 0
        tests = ('Sphere test', 'Yukawa test', 'Gaussian test')
        for line in lines:
            line = line.strip()
            if 'center grid points:' in line:
                data['Central grid size'] = int(line.split()[3])
            if 'number of points per interval:' in line:
                n_radial = int(line.split()[5])
            if 'total angular numbers of points:' in line:
                data['Atomic grid size'] = n_radial * int(line.split()[5])
            if 'percent diff:' in line:
                data[tests[test]] = float(line.split()[2])
                test += 1

        # Put any requested results into variables or tables
        self.store_results(
            data=data,
            properties=amo_grid_step.properties,
            results=self.parameters['results'].value,
            create_tables=self.parameters['create tables'].get()
        )
