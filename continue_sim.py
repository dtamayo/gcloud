#!/usr/bin/env python
# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import argparse
import rebound

def _parse_args():
    parser = argparse.ArgumentParser('continue_sim', 
                                     description='continue REBOUND integration')

    parser.add_argument('-f', 
                        '--filename', 
                        required=True, 
                        help='named of REBOUND binary to continue')

    return parser.parse_args()


def main():
    args = _parse_args()
    sa = rebound.SimulationArchive(args.filename)
    sim = sa[0]
    P0 = sim.particles[1].P
    sim = sa[-1]
    sim.automateSimulationArchive(args.filename, interval=1e5*P0)

    try:
        sim.integrate(sim.t + 1e6*P0) # hardcoded to run for a billion orbits
    except rebound.Collision:
        sim.simulationarchive_snapshot(args.filename)

if __name__ == '__main__':
    main()
