import { useI18n } from "vue-i18n";
import { computed } from "vue";

export const useOrbitNames = () => {
  const { t, locale } = useI18n();

  const tagToFamilyName = computed(() => ({
    "L1.L": t('families["L1.L"]'),
    "L1.V": t('families["L1.V"]'),
    "L1.H_s": t('families["L1.H_s"]'),
    "L1.H_n": t('families["L1.H_n"]'),
    "L1.L.2P1": t('families["L1.L.2P1"]'),
    "L1.L.3P1": t('families["L1.L.3P1"]'),
    "L1.L.4P1": t('families["L1.L.4P1"]'),
    "L1.L.2P1.2P1": t('families["L1.L.2P1.2P1"]'),
    "L1.Planar.2P1.2P1": t('families["L1.Planar.2P1.2P1"]'),
    "L1.Planar.2P1.3P1": t('families["L1.Planar.2P1.3P1"]'),
    "L1.Planar.2P1.3P2": t('families["L1.Planar.2P1.3P2"]'),
    "L1.H_n.2P2": t('families["L1.H_n.2P2"]'),
    // 'L1.H_n.3P1': t('families["L1.H_n.3P1"]'),
    // 'L1.H_n.3P2': t('families["L1.H_n.3P2"]'),
    "L1.H_n.3P3": t('families["L1.H_n.3P3"]'),
    // 'L1.H_n.4P1': t('families["L1.H_n.4P1"]'),
    "L1.H_s.2P1": t('families["L1.H_s.2P1"]'),
    "L1.H_s.2P3": t('families["L1.H_s.2P3"]'),
    "L1.H_s.3P1": t('families["L1.H_s.3P1"]'),
    "L1.H_s.3P2": t('families["L1.H_s.3P2"]'),
    "L1.H_s.3P3": t('families["L1.H_s.3P3"]'),
    // 'L1.H_s.4P1': t('families["L1.H_s.4P1"]'),
    // 'L1.Q': t('families["L1.Q"]'),

    "L2.L": t('families["L2.L"]'),
    "L2.V": t('families["L2.V"]'),
    "L2.H_s": t('families["L2.H_s"]'),
    "L2.H_n": t('families["L2.H_n"]'),
    "L2.L.2P1": t('families["L2.L.2P1"]'),
    "L2.L.3P1": t('families["L2.L.3P1"]'),
    "L2.L.4P1": t('families["L2.L.4P1"]'),
    "L2.L.2P1.2P1": t('families["L2.L.2P1.2P1"]'),
    "L2.Planar.2P1.2P1": t('families["L2.Planar.2P1.2P1"]'),
    "L2.Planar.2P1.3P1": t('families["L2.Planar.2P1.3P1"]'),
    "L2.Planar.2P1.3P2": t('families["L2.Planar.2P1.3P2"]'),
    "L2.H_n.2P2": t('families["L2.H_n.2P2"]'),
    "L2.H_n.3P1": t('families["L2.H_n.3P1"]'),
    "L2.H_s.2P1": t('families["L2.H_s.2P1"]'),
    "L2.H_s.3P1": t('families["L2.H_s.3P1"]'),
  }));

  const familyToTagL1 = computed(() => ({
    [t('families["L1.L"]')]: "L",
    [t('families["L1.V"]')]: "V",
    [t('families["L1.H_s"]')]: "H_s",
    [t('families["L1.H_n"]')]: "H_n",
    [t('families["L1.L.2P1"]')]: "L.2P1",
    [t('families["L1.L.3P1"]')]: "L.3P1",
    [t('families["L1.L.4P1"]')]: "L.4P1",
    [t('families["L1.L.2P1.2P1"]')]: "L.2P1.2P1",
    [t('families["L1.Planar.2P1.2P1"]')]: "Planar.2P1.2P1",
    [t('families["L1.Planar.2P1.3P1"]')]: "Planar.2P1.3P1",
    [t('families["L1.Planar.2P1.3P2"]')]: "Planar.2P1.3P2",
    [t('families["L1.H_n.2P2"]')]: "H_n.2P2",
    // [t('families["L1.H_n.3P1"]')]: 'H_n.3P1',
    // [t('families["L1.H_n.3P2"]')]: 'H_n.3P2',
    [t('families["L1.H_n.3P3"]')]: "H_n.3P3",
    // [t('families["L1.H_n.4P1"]')]: 'H_n.4P1',
    [t('families["L1.H_s.2P1"]')]: "H_s.2P1",
    [t('families["L1.H_s.2P3"]')]: "H_s.2P3",
    [t('families["L1.H_s.3P1"]')]: "H_s.3P1",
    [t('families["L1.H_s.3P2"]')]: "H_s.3P2",
    [t('families["L1.H_s.3P3"]')]: "H_s.3P3",
    // [t('families["L1.H_s.4P1"]')]: 'H_s.4P1',
    // [t('families["L1.Q"]')]: 'Q',
  }));

  const familyToTagL2 = computed(() => ({
    [t('families["L2.L"]')]: "L",
    [t('families["L2.V"]')]: "V",
    [t('families["L2.H_s"]')]: "H_s",
    [t('families["L2.H_n"]')]: "H_n",
    [t('families["L2.L.2P1"]')]: "L.2P1",
    [t('families["L2.L.3P1"]')]: "L.3P1",
    [t('families["L2.L.4P1"]')]: "L.4P1",
    [t('families["L2.L.2P1.2P1"]')]: "L.2P1.2P1",
    [t('families["L2.Planar.2P1.2P1"]')]: "Planar.2P1.2P1",
    [t('families["L2.Planar.2P1.3P1"]')]: "Planar.2P1.3P1",
    [t('families["L2.Planar.2P1.3P2"]')]: "Planar.2P1.3P2",
    [t('families["L2.H_n.2P2"]')]: "H_n.2P2",
    [t('families["L2.H_n.3P1"]')]: "H_n.3P1",
    [t('families["L2.H_s.2P1"]')]: "H_s.2P1",
    [t('families["L2.H_s.3P1"]')]: "H_s.3P1",
  }));

  return {
    tagToFamilyName,
    familyToTagL1,
    familyToTagL2,
  };
};
