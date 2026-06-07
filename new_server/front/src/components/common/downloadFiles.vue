<template>
    <div>
        <div class="button" :class="{ 'highlight-button': isOpenedOverlay }">
            <img class="icon" @click="switchOverlay" :src=download alt="svg">
        </div>

        <div v-if="isOpenedOverlay" class="overlay" :style="{ height: `${setHeight}px` }">
            <div class="close-btn" @click="switchOverlay">
                <img v-if="currentTheme.value === 'light'" class="cross" :src=Сross alt="svg" >
                <img v-else class="cross" :src=CrossDark alt="svg">
            </div>

            <div class="title-box">
                {{ $t('download.download_data') }}
            </div>

            <div class="container-for-selector" style="margin-bottom: 15px;">
                <div class="selector">
                    <div class="selector-option" :class="{ 'selected': selectedOption === 'calculations' }" @click="setOption('calculations')" style="width: 38%">
                        {{ $t('download.for_calculations') }}
                    </div>
                    <div class="selector-option" :class="{ 'selected': selectedOption === 'database' }"  @click="setOption('database')" style="width: 40%">
                        {{ $t('download.from_DB') }}
                    </div>
                    <div class="selector-option" :class="{ 'selected': selectedOption === 'scripts' }"  @click="setOption('scripts')" style="width: 22%">
                        {{ $t('download.scripts') }}
                    </div>
                </div>
            </div>

            <div v-if="selectedOption === 'database'" class="content">
                <div class="points">
                    <text>{{ $t('download.what_return') }}</text>
                    <div class="inputs">
                        <p>
                            <input type="radio" name="point3" value="orbits" checked v-model="formData.whatReturn"/>{{ $t('download.orbits') }}
                        </p>
                        <p>
                            <input type="radio" name="point3" value="trajectory" v-model="formData.whatReturn"/>{{ $t('download.trajectory') }}
                        </p>
                        <p>
                            <input type="radio" name="point3" value="sections" v-model="formData.whatReturn"/>{{ $t('download.sections') }}
                        </p>
                    </div>
                </div>
            </div>

            <div v-if="selectedOption !== 'scripts'" class="content">
                <div class="points">
                    <text>{{ $t('common.point') }}</text>
                    <div class="inputs">
                        <p>
                            <input type="radio" name="point2" value="L1" checked v-model="formData.point"/>{{ $t('common.system') }} L1
                        </p>
                        <p>
                            <input type="radio" name="point2" value="L2" v-model="formData.point"/>{{ $t('common.system') }} L2
                        </p>
                    </div>
                </div>

                <div class="vertical-group">
                    <text>{{ $t('common.family') }}</text>
                    <CustomSelect v-if="formData.point==='L1'"
                    v-model="formData.selectedFamily"
                    :options="Object.keys(familyToTagL1)"
                    width="262px"
                    style="z-index: 250"
                    ></CustomSelect>
                    <CustomSelect v-else
                    v-model="formData.selectedFamily"
                    :options="Object.keys(familyToTagL2)"
                    width="262px"
                    style="z-index: 250"
                    ></CustomSelect>
                </div>
            </div>

            <div v-if="selectedOption === 'database'" class="content" style="margin-top: 7px">
                <div class="vertical-group">
                    <text>{{ $t('download.parameter') }}</text>
                    <CustomSelect
                    v-model="formData.param"
                    :options="Object.keys(params)"
                    width="262px"
                    style="z-index: 240"
                    :maxVisibleOptions=4
                    ></CustomSelect>
                </div>

                <div class="input-group">
                    <text class="values">{{ $t('download.values') }}</text>
                    <validatedInput :placeholder="t('download.from')" fields="paramMin" @input-changed="updateValue"></validatedInput>
                    <text>—</text>
                    <validatedInput :placeholder="t('download.to')" fields="paramMax" @input-changed="updateValue"></validatedInput>
                </div>
            </div>

            <div v-if="selectedOption === 'scripts'" style="margin-left: 15px">
                {{ $t('download.just_press') }}
            </div>

            <div v-if="isOpenedOverlay">
                <a v-if="selectedOption === 'calculations'" :href="getUrlForCalculations" class="button-download">{{ $t('download.download') }}</a>
                <a v-if="selectedOption === 'scripts'" :href="getUrlForScripts" class="button-download">{{ $t('download.download') }}</a>
                <a v-else :href="getUrlForDatabase" class="button-download">{{ $t('download.download') }}</a>
            </div>
        </div>
    </div>
</template>

<script>
import CustomSelect from './CustomSelect.vue'
import validatedInput from './validatedInput.vue'
import Сross from "../../assets/cross.svg"
import CrossDark from "../../assets/cross-dark.svg"
import download from "../../assets/download.svg"
import { useOrbitNames } from '../../constants/familiesAndTags.js'
import { useI18n } from 'vue-i18n'
import { computed } from 'vue'

export default {
    components: { CustomSelect, validatedInput },
        setup() {
        const { t, locale } = useI18n()

        const { tagToFamilyName, familyToTagL1, familyToTagL2 } = useOrbitNames()
        const params = computed(() => ({
            [t('parameters.initial_x')]: "x",
            [t('parameters.initial_z')]: "z",
            [t('parameters.initial_speed_y')]: "vy",
            [t('parameters.abs_v')]: "abs_v",
            [t('parameters.t')]: "t",
            [t('parameters.ax')]: "ax",
            [t('parameters.ay')]: "ay",
            [t('parameters.az')]: "az",
            [t('parameters.earth_dist')]: "dist_primary",
            [t('parameters.moon_dist')]: "dist_secondary",
            [t('parameters.jacobi')]: "cj",
            [t('parameters.stability')]: "stable"
        } ))
        return { t, locale, tagToFamilyName, familyToTagL1, familyToTagL2, params }
    },
    data() {
        return {
            download,
            Сross,
            CrossDark,
            selectedOption: 'calculations',
            isOpenedOverlay: false,
            formData: {
                point: 'L1',
                selectedFamily: this.tagToFamilyName["L1.L"],
                whatReturn: '',
                param: this.t('parameters.initial_x'),
                paramMin: '',
                paramMax: ''
            }
        }
    },
    inject: ['theme'],
    computed: {
        currentTheme() {
            return this.theme?.currentTheme || 'light'
        },
        getUrlForCalculations(){
            let familyTag;

            if(this.formData.point==='L1'){
                familyTag = this.familyToTagL1[this.formData.selectedFamily]
            }
            else{
                familyTag = this.familyToTagL2[this.formData.selectedFamily]
            }

            return `${this.$AppURL}/download/get_data_for_script?lib_point=${this.formData.point}&family=${familyTag}`
        },
        getUrlForDatabase(){
            let familyTag;

            if(this.formData.point==='L1'){
                familyTag = this.familyToTagL1[this.formData.selectedFamily]
            }
            else{
                familyTag = this.familyToTagL2[this.formData.selectedFamily]
            }

            return `${this.$AppURL}/download/get_data_from_DB?what_return=${this.formData.whatReturn}&lib_point=${this.formData.point}&family=${familyTag}&param=${this.formData.param}&param_start=${this.formData.paramMin}&param_end=${this.formData.paramMax}`
        },
        getUrlForScripts(){
            return `${this.$AppURL}/download/get_script`
        },
        setHeight(){
            if(this.selectedOption==='calculations') return '400'
            if(this.selectedOption==='database') return '480'
            return '400'
        }
    },
    watch: {
        'formData.point': {
        handler(newPoint) {
            if(newPoint === 'L1' & this.familyToTagL1[this.formData.selectedFamily] === undefined){
            this.formData.selectedFamily = this.tagToFamilyName["L1.L"]
            }
            if(newPoint === 'L2' & this.familyToTagL2[this.formData.selectedFamily] === undefined){
            this.formData.selectedFamily = this.tagToFamilyName["L2.L"]
            }
        },
        immediate: true
        },
        'familyToTagL1': {
            handler(newValue, oldValue) {
                if(this.formData.point !== 'L1') return
                if(oldValue === undefined) return;

                let tag = oldValue[this.formData.selectedFamily];

                this.formData.selectedFamily = this.tagToFamilyName[`${this.formData.point}.${tag}`]
            },
            immediate: true,
            deep: true
        },
        'familyToTagL2': {
            handler(newValue, oldValue) {
                if(this.formData.point !== 'L2') return
                if(oldValue === undefined) return;

                let tag = oldValue[this.formData.selectedFamily];

                this.formData.selectedFamily = this.tagToFamilyName[`${this.formData.point}.${tag}`]
            },
            immediate: true,
            deep: true
        },
        'params': {
            handler(newValue, oldValue) {
                let param_tag = oldValue[this.formData.param];

                let keys = Object.keys(newValue);
                for(let i = 0; i<keys.length; ++i){
                    if(newValue[keys[i]] === param_tag){
                        this.formData.param = keys[i];
                        break;
                    }
                }
            }
        }
    },
    methods: {
        switchOverlay(){
            this.isOpenedOverlay = !this.isOpenedOverlay
        },
        setOption(option){
            this.selectedOption=option
        },
        updateValue(fields, value){
            this.formData[fields] = value;
        }
    }
}
</script>

<style scoped>

text{
    color: var(--text-primary);
}

.button{
    width: 38px;
    height: 38px;
    z-index: 50;

    border: 2px solid var(--theme-toggle-border);
    border-radius: 8px;

    display: flex;
    justify-content: center;
    align-items: center;

    cursor: pointer;
}

.icon{
    height: 25px;
}

.overlay{
    width: 320px;
    border-radius: 15px;
    background: var(--bg-primary);
    box-shadow: 0px 0px 18px 2px var(--shadow-primary);

    position: fixed;
    bottom: 10px;
    left: 70px;
    z-index: 150;
    
    display: flex;
    flex-direction: column;
    justify-items: center;
}

.close-btn{
    position: absolute;
    right: 10px;
    top: 10px;

    cursor: pointer;
}

.title-box{
    height: 50px;
    font-size: 17px;
    font-weight: 500;
    color: var(--text-primary);

    display: flex;
    justify-content: center;
    align-items: center;
}

.container-for-selector{
    display: flex;
    justify-content: center;
    align-items: center;
}

.selector{
    width: 310px;
    height: 25px;
    background-color: var(--selector-color-inactive);
    border-radius: 12.5px;

    display: flex;
    flex-direction: row;
}

.selector-option{
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 14px;
    cursor: pointer;
}

.selector-option.selected{
    background-color: var(--selector-color-active);
    border-radius: 12.5px;
}

.content{
    margin: 0 15px 0 15px;
}

.points{
    display: flex;
    flex-direction: row;
}

.inputs{
    margin-left: 15px;
}

.inputs p {
  margin: 1px 0px 5px 0px;
  display: flex;
  align-items: center;
  color: var(--text-primary);
}

input[type="radio"]{
  appearance: none;
  -webkit-appearance: none;
  -moz-appearance: none;
}

input[type="radio"] {
  cursor: pointer;
  height: 16px;
  width: 16px;
  margin: 0px 7px 0px 0px;
  border: 2px solid var(--select-border);
  border-radius: 50%;
  background-color: var(--radio-bg-color);
  position: relative;
  flex-shrink: 0;
}

input[type="radio"]:checked {
  background-color: var(--highlight-color);
  border-color: var(--highlight-color);
}

input[type="radio"]:checked::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 6px;
  height: 6px;
  background-color: var(--radio-inside-color);
  border-radius: 50%;
}

.vertical-group{
    display: flex;
    flex-direction: column;
    gap: 3px
}

.input-group{
    margin-top: 5px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 12px;
}

.values{
    width: 100px;
}

.button-download{
  width: 200px;
  height: 35px;
  cursor: pointer;
  background: var(--highlight-color);
  border-radius: 10px;
  margin-left: 60px;
  position: absolute;
  bottom: 10px;
  color: var(--text-button-able);
  font-size: 17px;
  z-index: 160;
  text-decoration: none;
  display: flex;
  justify-content: center;
  align-items: center;
}

.highlight-button{
    background-color: var(--download-button-bg);
}

</style>