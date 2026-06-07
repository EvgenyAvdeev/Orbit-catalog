<template>
    <div class="navigation-container">
        <router-link :to="{ path: '/orbit', query: { x: prevNextOrbit.prev.x, z: prevNextOrbit.prev.z, gradient: graphParams.gradientName, color_param: graphParams.parameter, graph: graphParams.graphType, settings: graphParams.settings, plane: graphParams.plane } }" @click="throwEmit">
            <img v-if="currentTheme.value === 'light'" class="icon" :src="to_left">
            <img v-else class="icon" :src="to_left_dark">
        </router-link>

        <div class="container-icons">
            <router-link :to="{ path: '/map', query: { point: localPopUp.lib_point, families: localPopUp.family_tag, selected_points: `[[${localPopUp.x.toFixed(10)};${localPopUp.z.toFixed(10)}]]` }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon1">
                <img v-else class="icon" :src="icon1_dark">
            </router-link>

            <router-link :to="{ path: '/orbit_family', query: { point: localPopUp.lib_point, family: localPopUp.family_tag, selected_points: `[[${localPopUp.t.toFixed(10)};${localPopUp.cj.toFixed(10)}]]` }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon3">
                <img v-else class="icon" :src="icon3_dark">
            </router-link>

            <router-link :to="{ path: '/cj', query: { point: localPopUp.lib_point, cj: (localPopUp.cj || 2.958).toFixed(5), selected_points: localPopUp.selectedPoints4thPage }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon4">
                <img v-else class="icon" :src="icon4_dark">
            </router-link>
        </div>
        
        <router-link :to="{ path: '/orbit', query: { x: prevNextOrbit.next.x, z: prevNextOrbit.next.z, gradient: graphParams.gradientName, color_param: graphParams.parameter, graph: graphParams.graphType, settings: graphParams.settings, plane: graphParams.plane } }" @click="throwEmit">
            <img v-if="currentTheme.value === 'light'" class="icon" :src="to_right">
            <img v-else class="icon" :src="to_right_dark">
        </router-link>
    </div>
</template>

<script>
import icon1 from '../../assets/active/icon-1.svg'
import icon3 from '../../assets/active/icon-3.svg'
import icon4 from '../../assets/active/icon-4.svg'
import to_right from '../../assets/active/to-right.svg'
import to_left from '../../assets/active/to-left.svg'
import icon1_dark from '../../assets/active/icon-1-dark.svg'
import icon3_dark from '../../assets/active/icon-3-dark.svg'
import icon4_dark from '../../assets/active/icon-4-dark.svg'
import to_right_dark from '../../assets/active/to-right-dark.svg'
import to_left_dark from '../../assets/active/to-left-dark.svg'
import { PoincareTemplateArray } from '@/utils/validation.js'

export default {
    data() {
        return {
            localPopUp: this.transferInfo,
            icon1,
            icon3,
            icon4,
            icon1_dark,
            icon3_dark,
            icon4_dark,
            to_right,
            to_right_dark,
            to_left,
            to_left_dark
        };
    },
    props: {
        transferInfo: {
            type: Object,
            default: {
                x: 0,
                z: 0,
                cj: 2.958,
                t: 1,
                lib_point: 'L1',
                family_tag: '',
                selectedPoints4thPage: ''
            }
        },
        prevNextOrbit: {
            type: Object,
            default: {
                prev: { x: -1, z: 0 },
                next: { x: 1, z: 0 }
            }
        },
        graphParams: {
            type: Object,
            default: {}
        }
    },
    watch: {
        transferInfo: {
            async handler(newPopUp){
                setTimeout(() => this.localPopUp = newPopUp, 10);

                let response = await fetch(`${this.$AppURL}/orbit_poincare_view/get_by_cj?filter_groups=[{"log_op":"NONE", "filters":[{"field":"orbit_id", "op":"==", "value":"${newPopUp.orbit_id}"},{"field":"plane", "op":"==", "value":"y = 0"}]}]&rate=0.0001`);
                
                if (!response.ok) {
                throw new Error(`статус запроса: ${response.status}`);
                }
            
                let data = await response.json();
                let PoincareInfo = PoincareTemplateArray.parse(data)[0];

                let points = [];
                for(let i = 0; i < PoincareInfo.x_points.length; ++i){
                    points.push(`[${PoincareInfo.x_points[i].toFixed(10)};${PoincareInfo.z_points[i].toFixed(10)}]`);
                }
                newPopUp.selectedPoints4thPage = `[${points.join(';')}]`

                setTimeout(() => this.localPopUp = newPopUp, 10);
            }
        },
        prevNextOrbit: {
            handler(newprevNextOrbit){
                this.prevNextOrbit = newprevNextOrbit;
            }
        }
    },
    inject: ['theme'],
    computed: {
        currentTheme() {
            return this.theme?.currentTheme || 'light'
        }
    },
    methods: {
        throwEmit(){
             setTimeout(() => {
                this.$emit('update-graph');
            }, 50);
        }
    }
}
</script>

<style scoped>

.navigation-container {
    display: flex;
    justify-content: space-between;
    gap: 7px; 
}

.container-icons{
    width: 186px;
    height: 50px;
    display: flex;
    justify-content: space-between;
    margin-left: auto;
    margin-right: auto;
}

.icon{
    height: 55px;
    width: 55px;
    border-radius: 7px;
    box-shadow: 0px 0px 9px 1px var(--shadow-primary);
}

.navigation-button{
    cursor: pointer;
    border-width: 0;
    background-color: transparent;
}

</style>