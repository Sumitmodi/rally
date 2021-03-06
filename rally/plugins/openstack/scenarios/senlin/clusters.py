#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from rally import consts
from rally.plugins.openstack import scenario
from rally.plugins.openstack.scenarios.senlin import utils
from rally.task import validation


class SenlinClusters(utils.SenlinScenario):
    """Benchmark scenarios for Senlin clusters."""

    @validation.required_openstack(admin=True)
    @validation.required_services(consts.Service.SENLIN)
    @scenario.configure(context={"cleanup": ["senlin"]})
    def create_and_delete_profile_cluster(self, profile_spec,
                                          desired_capacity=0, min_size=0,
                                          max_size=-1, timeout=3600,
                                          metadata=None):
        """Create a profile and a cluster and then delete them.

        Measure the "senlin profile-create", "senlin profile-delete",
        "senlin cluster-create" and "senlin cluster-delete" commands
        performance.

        :param profile_spec: spec dictionary used to create profile
        :param desired_capacity: The capacity or initial number of nodes
                                 owned by the cluster
        :param min_size: The minimum number of nodes owned by the cluster
        :param max_size: The maximum number of nodes owned by the cluster.
                         -1 means no limit
        :param timeout: The timeout value in seconds for cluster creation
        :param metadata: A set of key value pairs to associate with the cluster
        """
        profile = self._create_profile(profile_spec)
        cluster = self._create_cluster(profile.id, desired_capacity,
                                       min_size, max_size, timeout, metadata)
        self._delete_cluster(cluster)
        self._delete_profile(profile)
