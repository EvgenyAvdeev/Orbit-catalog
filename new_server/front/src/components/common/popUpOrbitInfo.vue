<template>
    <div style="margin-top: 10px;">
        <text >{{ $t('orbit.header3') }}:</text>
        <div class="info-grid">
            <div v-if="!isInData('X')" class="info-group">
                <text class="info-description">{{ $t('parameters.initial_x') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.x || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div v-if="!isInData('Z')" class="info-group">
                <text class="info-description">{{ $t('parameters.initial_z') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.z || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div v-if="!isInData('vy')" class="info-group">
                <text class="info-description">{{ $t('other.initial_vy') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.vy || 0).toFixed(2) }} {{ $t('common.km/s') }}</text>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center">
                <text class="info-description">{{ $t('orbit.family') }}</text>
                <text class="orbit-info" style="text-align: right">{{ processFamily() || '-' }}</text>
            </div>
             <div v-if="!isInData('cj')" class="info-group">
                <text class="info-description">{{ $t('orbit.jacobi') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.cj || 0).toFixed(6) }}</text>
            </div>
             <div v-if="!isInData('t')" class="info-group">
                <text class="info-description">{{ $t('orbit.period') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.t || 0).toFixed(2) }} {{ $t('common.days') }}</text>
            </div>
            <div v-if="!isInData('ax')" class="info-group">
                <text class="info-description">{{ $t('orbit.ax') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.ax || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div v-if="!isInData('ay')" class="info-group">
                <text class="info-description">{{ $t('orbit.ay') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.ay || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div v-if="!isInData('az')" class="info-group">
                <text class="info-description">{{ $t('orbit.az') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.az || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
             <div v-if="!isInData('dist_primary')" class="info-group">
                <text class="info-description" style="max-width: 120px;">{{ $t('orbit.earth_dist') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.dist_primary || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div v-if="!isInData('dist_secondary')" class="info-group">
                <text class="info-description" style="max-width: 120px;">{{ $t('orbit.moon_dist') }}</text>
                <text class="orbit-info">{{ (this.orbitInfo.dist_secondary || 0).toFixed(2) }} {{ $t('common.km') }}</text>
            </div>
            <div class="info-group">
                <text class="info-description">{{ $t('orbit.stability') }}</text>
                <text class="orbit-info">{{ this.orbitInfo.stable === undefined ? '-' : (this.orbitInfo.stable ? $t('orbit.stable') : $t('orbit.not_stable')) }}</text>
            </div>
            
        </div>
    </div>
</template>

<script>
import { useOrbitNames } from '../../constants/familiesAndTags.js'
import { useI18n } from 'vue-i18n'

export default {
    setup() {
        const { t, locale } = useI18n();
        const { tagToFamilyName } = useOrbitNames()
        return { t, locale, tagToFamilyName }
    },
    props: {
        orbitInfo: {
            type: Object,
            default: {}
        },
        xAxesName: {
            type: String,
            default: 'X'
        },
        yAxesName: {
            type: String,
            default: 'Y'
        }
    },
    methods: {
        isInData(name){
            return name === this.xAxesName | name === this.yAxesName;
        },
        processFamily(){
            let familyName = this.tagToFamilyName[`${this.orbitInfo.lib_point}.${this.orbitInfo.family_tag}`];

            if(familyName === undefined) return '-';
            let words = familyName.split(' ');
            
            let vowels;
            if(this.locale === 'ru'){
                vowels = new Set(['ё', 'й', 'у', 'е', 'ъ', 'ы', 'а', 'о', 'э', 'я', 'и', 'ь', 'ю']);
            }
            else{
                vowels = new Set(['q', 'e', 'y', 'u', 'i', 'o', 'a', 'j']);
            }
            
            for(let i=0; i<words.length; ++i){
                let end = 15;

                if(words[i].length>16){
                    for(let j=15; j>=0; --j){
                        if(!vowels.has(words[i][j])){
                            end = j;
                            break;
                        }
                    }
                    words[i] = words[i].slice(0, end+1) + '.';
                }
            }
            return words.join(' ');
        }
    }
}
</script>

<style scoped>
.info-grid {
  margin-top: 5px;
  display: grid;
  gap: 6px 6px;
}

.info-group {
    display: contents;
    display: flex;
    justify-content: space-between;
}

.info-description {
    font-size: 15px;
    grid-column: 1;
    color: var(--text-primary);
}

.orbit-info {
    font-size: 15px;
    grid-column: 2;
    color: var(--text-orbit-info);
}
</style>