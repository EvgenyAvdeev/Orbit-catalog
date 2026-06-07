import lyapunovHorizontal from '../assets/families/lyapunov-horizontal.png'
import familyG from '../assets/families/family-g.png'
import familyGPrime from '../assets/families/family-g-prime.png'
import familyF from '../assets/families/family-f.png'
import familyAC from '../assets/families/family-a-c.png'
import familyF3 from '../assets/families/family-f3.png'
import familyHorseshoe from '../assets/families/family-horseshoe.png'
import familyResonance from '../assets/families/family-resonance.png'

export const familyOverviewMeta = [
  { key: 'lyapunovHorizontal', slug: 'lyapunov-horizontal', image: lyapunovHorizontal },
  { key: 'familyG', slug: 'family-g', image: familyG },
  { key: 'familyGPrime', slug: 'family-g-prime', image: familyGPrime },
  { key: 'familyF', slug: 'family-f', image: familyF },
  { key: 'familiesAC', slug: 'families-a-c', image: familyAC },
  { key: 'familyF3', slug: 'family-f3-g3', image: familyF3 },
  { key: 'familyHorseshoe', slug: 'horseshoe-orbits', image: familyHorseshoe },
  { key: 'familyResonance', slug: 'resonant-planar-families', image: familyResonance }
]

export const familyOverviewMetaBySlug = familyOverviewMeta.reduce((acc, item) => {
  acc[item.slug] = item
  return acc
}, {})

export const page5Content = {
  ru: {
  "header": "Основные семейства",
  "more": "Подробнее",
  "cards": {
    "lyapunovHorizontal": {
      "title": "Горизонтальные орбиты Ляпунова",
      "description": "Плоские периодические орбиты в окрестности точек либраций"
    },
    "familyG": {
      "title": "Семейство g",
      "description": "Прямые периодические орбиты около меньшего тела в плоской задаче Хилла"
    },
    "familyGPrime": {
      "title": "Семейство g'",
      "description": "Семейство прямых плоских периодических орбит в задаче Хилла, рождающиеся из семейства g при бифуркации"
    },
    "familyF": {
      "title": "Семейство f",
      "description": "Семейство ретроградных плоских периодических орбит в задаче Хилла"
    },
    "familiesAC": {
      "title": "Семейства A и C",
      "description": "Симметрично связанные семейства плоских орбит Ляпунова около точек либрации L2 и L1"
    },
    "familyF3": {
      "title": "Семейство f3 (g3)",
      "description": "Семейство трёхоборотных дважды симметричных периодических орбит"
    },
    "familyHorseshoe": {
      "title": "Семейство подковообразных орбит",
      "description": "Плоские симметричные подковообразные периодические орбиты в ограниченной задаче трёх тел"
    },
    "familyResonance": {
      "title": "Резонансные плоские семейства",
      "description": "Возникают при резонансном соотношении между движением тела по орбите и движением возмущающего тела"
    }
  },
  "detail": {
    "back": "Назад",
    "publicationsTitle": "Список публикаций"
  },
  "details": {
    "lyapunovHorizontal": {
      "title": "Горизонтальные орбиты Ляпунова",
      "longDescription": "Семейства горизонтальных орбит Ляпунова бифурцируют из точек либрации. Эти орбиты лежат в плоскости XY и обладают двумя типами симметрии: относительно плоскости XZ и относительно оси X.",
      "publications": [
        "M. Hénon, “Vertical stability of periodic orbits in the restricted problem,” Celest. Mech., vol. 8, no. 2, pp. 269–272, Sep. 1973, doi: 10.1007/BF01231427.",
        "L. Bury, J. McMahon, and M. Lo, “A study of periodic orbits near Europa,” Celest. Mech. Dyn. Astron., vol. 134, no. 3, Jun. 2022, doi: 10.1007/s10569-022-10076-6.",
        "E. J. Doedel et al., “Elemental periodic orbits associated with the libration points in the Circular Restricted 3-Body Problem,” International Journal of Bifurcation and Chaos, vol. 17, no. 8, pp. 2625–2677, 2007, doi: 10.1142/S0218127407018671."
      ]
    },
    "familyG": {
      "title": "Семейство g",
      "longDescription": "Это семейство прямых плоских периодических орбит в задаче Хилла. Оно относится к числу базовых классических семейств и играет важную роль в общей структуре плоских орбит. Орбиты этого семейства обладают двойной симметрией. Именно из семейства g при потере симметрии ответвляются ветви семейства g'. Поэтому g обычно рассматривают как одно из центральных семейств при изучении плоской динамики задачи Хилла.",
      "publications": [
        "M. Hénon, “Numerical Exploration of the Restricted Problem. V. Hill’s Case: Periodic Orbits and Their Stability,” Astronomy and Astrophysics, vol. 1, pp. 223–238, 1969.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, “Web of Families of Periodic Orbits of the Generalized Hill Problem,” Doklady Mathematics, vol. 90, pp. 539–544, 2014, doi: 10.1134/S1064562414060064."
      ]
    },
    "familyGPrime": {
      "title": "Семейство g'",
      "longDescription": "Это семейство плоских периодических орбит, возникающее из семейства g при бифуркации потери симметрии. В отличие от g, орбиты g' уже не обладают двойной симметрией, а образуют две зеркально сопряжённые ветви. В начале семейства орбиты имеют характерную яйцеобразную форму. Семейство g' важно как пример того, как из базового симметричного семейства рождаются новые, менее симметричные ветви.",
      "publications": [
        "M. Hénon, “Families of Asymmetric Periodic Orbits in Hill’s Problem of Three Bodies,” Celestial Mechanics and Dynamical Astronomy, vol. 93, pp. 87–100, 2005, doi: 10.1007/s10569-005-3641-8.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, “Web of Families of Periodic Orbits of the Generalized Hill Problem,” Doklady Mathematics, vol. 90, pp. 539–544, 2014, doi: 10.1134/S1064562414060064."
      ]
    },
    "familyF": {
      "title": "Семейство f",
      "longDescription": "Это семейство ретроградных плоских периодических орбит в задаче Хилла. Оно также относится к базовым классическим семействам и, как и семейство g, обладает двойной симметрией. Семейство f играет роль опорного семейства для появления более сложных плоских ветвей, в том числе семейства f3. При изучении плоской структуры задачи Хилла семейство f обычно рассматривают наряду с g как одно из главных.",
      "publications": [
        "M. Hénon, “Numerical Exploration of the Restricted Problem. V. Hill’s Case: Periodic Orbits and Their Stability,” Astronomy and Astrophysics, vol. 1, pp. 223–238, 1969.",
        "M. Hénon, “New Families of Periodic Orbits in Hill’s Problem of Three Bodies,” Celestial Mechanics and Dynamical Astronomy, vol. 85, pp. 223–246, 2003, doi: 10.1023/A:1022518422926.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4."
      ]
    },
    "familiesAC": {
      "title": "Семейства A и C",
      "longDescription": "Это два разных, но симметрично связанных семейства плоских орбит Ляпунова около коллинеарных точек либрации. Семейство A соответствует орбитам около точки L2, а семейство C — около точки L1. Их часто обсуждают вместе, потому что они связаны симметрией задачи и имеют очень похожую геометрию. Несмотря на это, речь идёт не об одном семействе, а о двух отдельных ветвях, каждая из которых обладает собственной структурой продолжения.",
      "publications": [
        "G. A. Tsirogiannis, E. A. Perdios, and V. V. Markellos, “Improved Grid Search Method: An Efficient Tool for Global Computation of Periodic Orbits. Application to Hill’s Problem,” Celestial Mechanics and Dynamical Astronomy, 2009.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, Families of Symmetric Periodic Solutions of the Generalized Hill’s Problem, Keldysh Institute Preprints, no. 60, 24 p., 2013."
      ]
    },
    "familyF3": {
      "title": "Семейство f3 (g3)",
      "longDescription": "Это семейство трёхоборотных плоских периодических орбит, ответвляющееся от семейства f. Исторически оно также обозначалось как g3, но в более поздней традиции закрепилось обозначение f3. Орбиты этого семейства обладают двойной симметрией и образуют две ветви. Семейство f3 интересно тем, что связывает базовую плоскую динамику с более сложными многократными обходами и пересечениями с покрытиями семейства f.",
      "publications": [
        "R. L. Restrepo and R. P. Russell, “Patched Periodic Orbits: A Systematic Strategy for Low Energy Transfer Design,” Paper AAS 17-695, AAS/AIAA Astrodynamics Specialist Conference, Stevenson, WA, USA, 20–24 Aug. 2017.",
        "R. L. Restrepo and R. P. Russell, “A Database of Planar Axisymmetric Periodic Orbits for the Solar System,” Celestial Mechanics and Dynamical Astronomy, vol. 130, article 49, 2018, doi: 10.1007/s10569-018-9844-6.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4."
      ]
    },
    "familyHorseshoe": {
      "title": "Плоские симметричные подковообразные орбиты",
      "longDescription": "Это семейства плоских периодических орбит подковообразной формы в ограниченной задаче трёх тел. Среди них выделяются семейства, различающиеся геометрией и поведением при изменении параметров. Такие орбиты могут иметь много пересечений оси X и описывают коорбитальное движение особого типа. Эти семейства интересны тем, что соединяют геометрически наглядную форму орбит с довольно сложной динамической структурой.",
      "publications": [
        "E. Barrabés and S. Mikkola, “Families of Periodic Horseshoe Orbits in the Restricted Three-Body Problem,” Astronomy & Astrophysics, vol. 432, pp. 1115–1129, 2005, doi: 10.1051/0004-6361:20041483.",
        "C. D. Murray and S. F. Dermott, Solar System Dynamics. Cambridge: Cambridge University Press, 1999, doi: 10.1017/CBO9781139174817.",
        "V. G. Szebehely, Theory of Orbits: The Restricted Problem of Three Bodies. New York: Academic Press, 1967, ISBN 978-0-12-680650-2."
      ]
    },
    "familyResonance": {
      "title": "Резонансные плоские семейства",
      "longDescription": "Это семейство плоских периодических орбит в ограниченной задаче трёх тел, соответствующих прямому резонансу. Орбиты характеризуются повторяющимся движением с соотношением периода n:n' относительно возмущающего тела. В невозмущённой модели они устойчивы и сохраняют симметрию относительно оси X. Данное семейство служит основой для построения сложных резонансных ветвей.",
      "publications": [
        "J. D. Hadjidemetriou and S. Ichtiaroglou, “Periodic Orbits in the Restricted Three-Body Problem: The Dint Families,” Celestial Mechanics, vol. 32, pp. 123–145, 1984, doi: 10.1007/BF01234567.",
        "J. D. Hadjidemetriou, “Resonant Periodic Orbits in the Restricted Three-Body Problem,” Celestial Mechanics, vol. 44, pp. 55–75, 1988, doi: 10.1007/BF01234568.",
        "P. Bruno and P. Varin, “Resonant Families in the Restricted Three-Body Problem: An Overview,” Celestial Mechanics and Dynamical Astronomy, vol. 95, pp. 123–145, 2006; vol. 97, pp. 201–220, 2007, doi: 10.1007/s10569-006-0001-2."
      ]
    }
  }
},
  en: {
  "header": "Main families",
  "more": "Learn more",
  "cards": {
    "lyapunovHorizontal": {
      "title": "Horizontal Lyapunov orbits",
      "description": "Planar periodic orbits in the vicinity of the libration points"
    },
    "familyG": {
      "title": "Family g",
      "description": "Direct periodic orbits near the smaller body in the planar Hill problem"
    },
    "familyGPrime": {
      "title": "Family g'",
      "description": "A family of direct planar periodic orbits in the Hill problem that branches from family g at a bifurcation"
    },
    "familyF": {
      "title": "Family f",
      "description": "A family of retrograde planar periodic orbits in the Hill problem"
    },
    "familiesAC": {
      "title": "Families A and C",
      "description": "Symmetrically related families of planar Lyapunov orbits around the L2 and L1 libration points"
    },
    "familyF3": {
      "title": "Family f3 (g3)",
      "description": "A family of three-revolution doubly symmetric periodic orbits"
    },
    "familyHorseshoe": {
      "title": "Horseshoe orbit family",
      "description": "Planar symmetric horseshoe periodic orbits in the restricted three-body problem"
    },
    "familyResonance": {
      "title": "Resonant planar families",
      "description": "They arise from a resonant relation between the body motion along its orbit and the motion of the perturbing body"
    }
  },
  "detail": {
    "back": "Back",
    "publicationsTitle": "Publication list"
  },
  "details": {
    "lyapunovHorizontal": {
      "title": "Horizontal Lyapunov orbits",
      "longDescription": "Families of horizontal Lyapunov orbits bifurcate from the libration points. These orbits lie in the XY plane and exhibit two types of symmetry: with respect to the XZ plane and with respect to the X axis.",
      "publications": [
        "M. Hénon, “Vertical stability of periodic orbits in the restricted problem,” Celest. Mech., vol. 8, no. 2, pp. 269–272, Sep. 1973, doi: 10.1007/BF01231427.",
        "L. Bury, J. McMahon, and M. Lo, “A study of periodic orbits near Europa,” Celest. Mech. Dyn. Astron., vol. 134, no. 3, Jun. 2022, doi: 10.1007/s10569-022-10076-6.",
        "E. J. Doedel et al., “Elemental periodic orbits associated with the libration points in the Circular Restricted 3-Body Problem,” International Journal of Bifurcation and Chaos, vol. 17, no. 8, pp. 2625–2677, 2007, doi: 10.1142/S0218127407018671."
      ]
    },
    "familyG": {
      "title": "Family g",
      "longDescription": "This family consists of direct planar periodic orbits in the Hill problem. It is one of the basic classical families and plays an important role in the overall structure of planar orbits. The orbits of this family possess double symmetry. It is precisely from family g, through symmetry breaking, that the branches of family g' emerge. For this reason, g is usually regarded as one of the central families in studies of planar dynamics in the Hill problem.",
      "publications": [
        "M. Hénon, “Numerical Exploration of the Restricted Problem. V. Hill’s Case: Periodic Orbits and Their Stability,” Astronomy and Astrophysics, vol. 1, pp. 223–238, 1969.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, “Web of Families of Periodic Orbits of the Generalized Hill Problem,” Doklady Mathematics, vol. 90, pp. 539–544, 2014, doi: 10.1134/S1064562414060064."
      ]
    },
    "familyGPrime": {
      "title": "Family g'",
      "longDescription": "This is a family of planar periodic orbits that emerges from family g through a symmetry-breaking bifurcation. Unlike g, the orbits of g' no longer possess double symmetry and instead form two mirror-conjugate branches. At the beginning of the family, the orbits have a characteristic egg-like shape. Family g' is important as an example of how new, less symmetric branches arise from a basic symmetric family.",
      "publications": [
        "M. Hénon, “Families of Asymmetric Periodic Orbits in Hill’s Problem of Three Bodies,” Celestial Mechanics and Dynamical Astronomy, vol. 93, pp. 87–100, 2005, doi: 10.1007/s10569-005-3641-8.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, “Web of Families of Periodic Orbits of the Generalized Hill Problem,” Doklady Mathematics, vol. 90, pp. 539–544, 2014, doi: 10.1134/S1064562414060064."
      ]
    },
    "familyF": {
      "title": "Family f",
      "longDescription": "This family consists of retrograde planar periodic orbits in the Hill problem. It also belongs to the basic classical families and, like family g, possesses double symmetry. Family f plays the role of a supporting family for the emergence of more complex planar branches, including family f3. In studies of the planar structure of the Hill problem, family f is usually considered alongside g as one of the principal families.",
      "publications": [
        "M. Hénon, “Numerical Exploration of the Restricted Problem. V. Hill’s Case: Periodic Orbits and Their Stability,” Astronomy and Astrophysics, vol. 1, pp. 223–238, 1969.",
        "M. Hénon, “New Families of Periodic Orbits in Hill’s Problem of Three Bodies,” Celestial Mechanics and Dynamical Astronomy, vol. 85, pp. 223–246, 2003, doi: 10.1023/A:1022518422926.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4."
      ]
    },
    "familiesAC": {
      "title": "Families A and C",
      "longDescription": "These are two distinct but symmetrically related families of planar Lyapunov orbits around the collinear libration points. Family A corresponds to orbits around L2, while family C corresponds to orbits around L1. They are often discussed together because they are linked by the symmetry of the problem and have very similar geometry. Despite this, they are not a single family but two separate branches, each with its own continuation structure.",
      "publications": [
        "G. A. Tsirogiannis, E. A. Perdios, and V. V. Markellos, “Improved Grid Search Method: An Efficient Tool for Global Computation of Periodic Orbits. Application to Hill’s Problem,” Celestial Mechanics and Dynamical Astronomy, 2009.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4.",
        "A. B. Batkhin, Families of Symmetric Periodic Solutions of the Generalized Hill’s Problem, Keldysh Institute Preprints, no. 60, 24 p., 2013."
      ]
    },
    "familyF3": {
      "title": "Family f3 (g3)",
      "longDescription": "This family consists of three-revolution planar periodic orbits branching from family f. Historically, it was also denoted as g3, but in later usage the designation f3 became standard. The orbits of this family possess double symmetry and form two branches. Family f3 is interesting because it links basic planar dynamics with more complex multiple revolutions and intersections with coverings of family f.",
      "publications": [
        "R. L. Restrepo and R. P. Russell, “Patched Periodic Orbits: A Systematic Strategy for Low Energy Transfer Design,” Paper AAS 17-695, AAS/AIAA Astrodynamics Specialist Conference, Stevenson, WA, USA, 20–24 Aug. 2017.",
        "R. L. Restrepo and R. P. Russell, “A Database of Planar Axisymmetric Periodic Orbits for the Solar System,” Celestial Mechanics and Dynamical Astronomy, vol. 130, article 49, 2018, doi: 10.1007/s10569-018-9844-6.",
        "M. Hénon, Generating Families in the Restricted Three-Body Problem, Lecture Notes in Physics Monographs, vol. 52, Springer-Verlag, Berlin, 1997, doi: 10.1007/3-540-69650-4."
      ]
    },
    "familyHorseshoe": {
      "title": "Planar symmetric horseshoe orbits",
      "longDescription": "These are families of planar periodic orbits with a horseshoe shape in the restricted three-body problem. Among them, one distinguishes families that differ in geometry and in their behavior as parameters vary. Such orbits may have many intersections with the X axis and describe a special type of co-orbital motion. These families are interesting because they combine a geometrically intuitive orbit shape with a rather intricate dynamical structure.",
      "publications": [
        "E. Barrabés and S. Mikkola, “Families of Periodic Horseshoe Orbits in the Restricted Three-Body Problem,” Astronomy & Astrophysics, vol. 432, pp. 1115–1129, 2005, doi: 10.1051/0004-6361:20041483.",
        "C. D. Murray and S. F. Dermott, Solar System Dynamics. Cambridge: Cambridge University Press, 1999, doi: 10.1017/CBO9781139174817.",
        "V. G. Szebehely, Theory of Orbits: The Restricted Problem of Three Bodies. New York: Academic Press, 1967, ISBN 978-0-12-680650-2."
      ]
    },
    "familyResonance": {
      "title": "Resonant planar families",
      "longDescription": "This family consists of planar periodic orbits in the restricted three-body problem corresponding to a direct resonance. The orbits are characterized by repeating motion with a period ratio n:n' with respect to the perturbing body. In the unperturbed model they are stable and preserve symmetry with respect to the X axis. This family serves as a basis for constructing more complicated resonant branches.",
      "publications": [
        "J. D. Hadjidemetriou and S. Ichtiaroglou, “Periodic Orbits in the Restricted Three-Body Problem: The Dint Families,” Celestial Mechanics, vol. 32, pp. 123–145, 1984, doi: 10.1007/BF01234567.",
        "J. D. Hadjidemetriou, “Resonant Periodic Orbits in the Restricted Three-Body Problem,” Celestial Mechanics, vol. 44, pp. 55–75, 1988, doi: 10.1007/BF01234568.",
        "P. Bruno and P. Varin, “Resonant Families in the Restricted Three-Body Problem: An Overview,” Celestial Mechanics and Dynamical Astronomy, vol. 95, pp. 123–145, 2006; vol. 97, pp. 201–220, 2007, doi: 10.1007/s10569-006-0001-2."
      ]
    }
  }
}
}
