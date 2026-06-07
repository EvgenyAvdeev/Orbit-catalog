<template>
  <div class="tooltip" v-if="newState !== 'OK'" :style="setNotifSizes">
    <text v-if="newState !== 'Loading'" style="color: var(--text-primary)">{{ stateToText[newState] }}</text>

    <div class="loading-container" v-else>
        <video autoplay loop muted playsinline preload="metadata">
            <source v-if="currentTheme.value === 'dark'" src="../../assets/loading-dark.mp4" type="video/mp4"> 
            <source v-else src="../../assets/loading.mp4" type="video/mp4">
        </video>
        <img src="../../assets/loading-preview.png">
        
        <text style="color: var(--text-primary);">{{ $t('other.loading') }}...</text>
    </div>
  </div>
</template>

<script>
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
    setup() {
        const { t, locale } = useI18n();

        const stateToText = computed(() => ({
            'ValidError': t('other.validation_error'),
            'noPointsError': t('other.no_points_error'),
            'unknownError': t('other.unknown_error')
        }))

        return { t, locale, stateToText }
    },
    data() {
        return {
            stateToWidthHeight: {
                'Loading': { 'width': '100px', 'height': '85px' },
                'ValidError': { 'width': 'auto', 'height': '20px' },
                'noPointsError': { 'width': 'auto', 'height': '20px' },
                'unknownError': { 'width': 'auto', 'height': '20px' }
            }
        }
    },
    props: {
        newState: {
            type: String,
            default: 'OK'
        }
    },
    watch: {
        newState: {
            handler(newState) {
                this.state = newState;
            }
        }
    },
    inject: ['theme'],
    computed: {
        setNotifSizes() {
            return this.stateToWidthHeight[this.newState];
        },
        currentTheme() {
            return this.theme?.currentTheme || 'light'
        }
    }
}
</script>

<style scoped>
.tooltip{
    display: flex;
    justify-content: center;
    background: var(--bg-primary);
    border-radius: 15px;
    box-shadow: 0px 0px 10px 2px var(--shadow-primary);
    padding: 15px;

    position: fixed;
    top: 45%;
    left: calc(43%-width*0.5);
    z-index: 50;
}

video {
    height: 70px;
    position: absolute;
    object-fit: cover;
}

img {
    height: 70px;
}

.loading-container{
    position: relative;
    text-align: center;
    padding-bottom: 5px;
    display: flex;
    flex-direction: column;
    gap: 0px;
}

</style>