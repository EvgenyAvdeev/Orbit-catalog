<template>
    <div ref="transferPopUp" class="popUp" :style="{ top: `${setTop}px`, left: `${setLeft}px`, width: 'auto' }" @blur="handleClickOutside">
        <p>X = {{ localPopUp.x.toFixed(5) }} {{ $t('common.km') }}</p>
        <p>Y = {{ localPopUp.y.toFixed(5) }} {{ $t('common.km') }}</p>
        <p>Z = {{ localPopUp.z.toFixed(5) }} {{ $t('common.km') }}</p>
        <p>|V| = {{ localPopUp.abs_v.toFixed(5) }} {{ $t('common.km/s') }}</p>
    </div>
</template>

<script>
import { useI18n } from 'vue-i18n'

export default {
    setup() {
        const { t, locale } = useI18n();
        return { t, locale }
    },
    data() {
        return {
            localPopUp: JSON.parse(JSON.stringify(this.popUp)), 
            initialPos: { 
                x: -1000, 
                y: 0
            },
            axisNameToMeasUnit: {
                'X': this.t('common.km'),
                'Y': this.t('common.km'),
                'Z': this.t('common.km'),
                'Vx': this.t('common.km/s'),
                'Vy': this.t('common.km/s'),
                'Vz': this.t('common.km/s'),
                'vy': this.t('common.km/s'),
                't': this.t('common.days'),
                'ax': this.t('common.km'),
                'ay': this.t('common.km'),
                'az': this.t('common.km'),
                'dist_primary': this.t('common.km'),
                'dist_secondary': this.t('common.km'),
                'cj': '',
                'floke': '',
                'α': '',
                'β': ''
            }
        };
    },
    props: {
        popUp: {
            type: Object,
            default: {
                x: 0,
                y: 0,
                z: 0,
                abs_v: 0,
                dataXInPixels: 0,
                dataYInPixels: 0,
                popUpX: -1000,
                popUpY: 0
            }
        }
    },
    watch: {
        popUp: {
            handler(newPopUp){
                setTimeout(() => this.localPopUp = newPopUp, 10);
                this.initialPos.x = newPopUp.popUpX;
                this.initialPos.y = newPopUp.popUpY;
            }
        }
    },
    mounted() {
        document.addEventListener('click', this.handleClickOutside);
    },
    beforeUnmount() {
        document.removeEventListener('click', this.handleClickOutside);
    },
    methods: {
        handleClickOutside(event) {
            if (this.localPopUp.popUpX !== -1000 && this.$el !== undefined && !this.$el.contains(event.target)) {
                this.localPopUp.popUpX = -1000;
                this.showOrbitInfo = false;
            }
        }
    },
    inject: ['theme'],
    computed: {
        setTop(){
            var currHeight = 140;
            var currPageHeight = document.documentElement.scrollHeight;

            if(this.localPopUp.popUpY + currHeight > currPageHeight){
                return currPageHeight - currHeight;
            }
            else{
                return this.localPopUp.popUpY;
            }
        },
        setLeft() {
            var currWidth = 160;
            this.$nextTick(() => {
                if(this.$refs.transferPopUp){
                    currWidth = this.$refs.transferPopUp.clientWidth;
                }
            });
            var firstApprox;

            if(this.localPopUp.popUpX <= this.localPopUp.dataXInPixels && this.localPopUp.dataXInPixels <= this.localPopUp.popUpX + currWidth){
                firstApprox = this.localPopUp.popUpX - currWidth - 5
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