<template>
    <div ref="transferPopUp" class="popUp" :style="{ top: `${setTop}px`, left: `${setLeft}px`, width: `${setWidth}px` }" @blur="handleClickOutside">
        <p>{{ $t('other.nearest_point') }}:</p>
        <p>{{ `${prepareName(localPopUp.xAxesName)} = ${localPopUp.dataX.toFixed(5)}`}} {{ `${axisNameToMeasUnit[localPopUp.xAxesName]}` }}</p>
        <p>{{ `${prepareName(localPopUp.yAxesName)} = ${localPopUp.dataY.toFixed(5)}`}} {{ `${axisNameToMeasUnit[localPopUp.yAxesName]}` }}</p>

        <popUpOrbitInfo v-if="showOrbitInfo" :orbitInfo="this.localPopUp" :xAxesName="localPopUp.xAxesName" :yAxesName="localPopUp.yAxesName"></popUpOrbitInfo>

        <div class="container-icons">
            <router-link v-if="currPageNumber !== 1" :to="{ path: '/map', query: { point: localPopUp.lib_point, families: localPopUp.family_tag, selected_points: `[[${localPopUp.x.toFixed(10)};${localPopUp.z.toFixed(10)}]]` }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon1">
                <img v-else class="icon" :src="icon1_dark">
            </router-link>

            <router-link v-if="currPageNumber !== 2" :to="{ path: '/orbit', query: { x: localPopUp.x.toFixed(5), z: localPopUp.z.toFixed(5) }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon2">
                <img v-else class="icon" :src="icon2_dark">
            </router-link>

            <router-link v-if="currPageNumber !== 3" :to="{ path: '/orbit_family', query: { point: localPopUp.lib_point, family: localPopUp.family_tag, selected_points: `[[${localPopUp.t.toFixed(10)};${localPopUp.cj.toFixed(10)}]]` }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon3">
                <img v-else class="icon" :src="icon3_dark">
            </router-link>

            <router-link v-if="currPageNumber !== 4" :to="{ path: '/cj', query: { point: localPopUp.lib_point, cj: localPopUp.cj.toFixed(5), selected_points: localPopUp.selectedPoints4thPage }}">
                <img v-if="currentTheme.value === 'light'" class="icon" :src="icon4">
                <img v-else class="icon" :src="icon4_dark">
            </router-link>
        </div>
    </div>
</template>

<script>
import icon1 from '../../assets/active/icon-1.svg'
import icon2 from '../../assets/active/icon-2.svg'
import icon3 from '../../assets/active/icon-3.svg'
import icon4 from '../../assets/active/icon-4.svg'
import icon1_dark from '../../assets/active/icon-1-dark.svg'
import icon2_dark from '../../assets/active/icon-2-dark.svg'
import icon3_dark from '../../assets/active/icon-3-dark.svg'
import icon4_dark from '../../assets/active/icon-4-dark.svg'
import popUpOrbitInfo from './popUpOrbitInfo.vue'
import { PoincareTemplateArray } from '@/utils/validation.js';
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
    components: { popUpOrbitInfo },
    setup() {
        const { t, locale } = useI18n();

        const axisNameToMeasUnit = computed(() => ({
            'X': t('common.km'),
            'Y': t('common.km'),
            'Z': t('common.km'),
            '|V|': t('common.km/s'),
            'Vx': t('common.km/s'),
            'Vy': t('common.km/s'),
            'Vz': t('common.km/s'),
            'vy': t('common.km/s'),
            't': t('common.days'),
            'ax': t('common.km'),
            'ay': t('common.km'),
            'az': t('common.km'),
            'dist_primary': t('common.km'),
            'dist_secondary': t('common.km'),
            'cj': '',
            'floke': '',
            'α': '',
            'β': '',
            'stable': '',
            'stability_ind_1': '',
            'stability_ind_2': '',
            'stability_ind_3': ''
        }))

        return { t, locale, axisNameToMeasUnit }
    },
    data() {
        return {
            localPopUp: JSON.parse(JSON.stringify(this.popUp)), 
            icon1,
            icon2,
            icon3,
            icon4,
            icon1_dark,
            icon2_dark,
            icon3_dark,
            icon4_dark,
            initialPos: { 
                x: -1000, 
                y: 0
            },
            showOrbitInfo: false
        };
    },
    props: {
        popUp: {
            type: Object,
            default: {
                x: 0,
                z: 0,
                cj: 2.958,
                t: 1,
                lib_point: 'L1',
                family_tag: '',
                dataX: 0,
                dataY: 0,
                dataXInPixels: 0,
                dataYInPixels: 0,
                popUpX: -1000,
                popUpY: 0,
                xAxesName: 'X',
                yAxesName: 'Y',
                selectedPoints4thPage: ''
            }
        },
        currPageNumber: {
            type: Number,
            default: 1
        }
    },
    watch: {
        popUp: {
            async handler(newPopUp){
                setTimeout(() => this.localPopUp = newPopUp, 10);
                this.initialPos.x = newPopUp.popUpX;
                this.initialPos.y = newPopUp.popUpY;

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
            }
        }
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
        document.addEventListener('keydown', this.handleShift);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
        document.removeEventListener('keydown', this.handleShift);
    },
    methods: {
        handleClickOutside(event) {
            if (this.localPopUp.popUpX !== -1000 && this.$el !== undefined && !this.$el.contains(event.target)) {
                this.localPopUp.popUpX = -1000;
                this.showOrbitInfo = false;
            }
        },
        handleShift(event) {
            if (event.key === 'Shift' || event.keyCode === 16) {
                if(!this.showOrbitInfo){
                    var currHeight = 480;
                    var currPageHeight = document.documentElement.scrollHeight;

                    if(this.localPopUp.popUpY + currHeight > currPageHeight){
                        this.localPopUp.popUpY = currPageHeight - currHeight;
                    }
                }
                else{
                    this.localPopUp.popUpY = this.initialPos.y;
                }
                this.showOrbitInfo = !this.showOrbitInfo;
            }
        },
        prepareName(name){
            return name.replace('stability_ind_', 'stab_ind')
        }
    },
    inject: ['theme'],
    computed: {
        setTop(){
            var currHeight = this.showOrbitInfo ? 516 : 140;
            var currPageHeight = document.documentElement.scrollHeight;

            if(this.localPopUp.popUpY + currHeight > currPageHeight){
                return currPageHeight - currHeight;
            }
            else{
                return this.localPopUp.popUpY;
            }
        },
        setLeft() {
            var currWidth = this.showOrbitInfo ? 256 : 206;
            var firstApprox;

            if(this.localPopUp.popUpX <= this.localPopUp.dataXInPixels && this.localPopUp.dataXInPixels <= this.localPopUp.popUpX + currWidth){
                firstApprox = this.localPopUp.popUpX - currWidth - 5;
            }
            else{
                firstApprox = this.localPopUp.popUpX
            }

            if(this.localPopUp.popUpX === -1000) return -1000;

            if(firstApprox<60){
                return 60;
            }
            else if(firstApprox+currWidth > document.documentElement.scrollWidth){
                return document.documentElement.scrollWidth-currWidth;
            }

            return firstApprox;
        },
        setWidth(){
            return this.showOrbitInfo ? 236 : 186;
        },
        currentTheme(){
            return this.theme?.currentTheme || 'light'
        }
    }
}
</script>

<style scoped>

p {
    margin: 0;
}

.popUp{
    position: absolute;
    background: var(--bg-primary);
    box-shadow: 0px 0px 10px 2px var(--shadow-primary);
    border-radius: 15px;
    padding: 10px;
    z-index: 75;
    color: var(--text-primary);
}

.container-icons{
    margin-top: 12px;
    width: 186px;
    height: 50px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-left: auto;
    margin-right: auto;
}

.icon{
    height: 55px;
    width: 55px;
}

</style>